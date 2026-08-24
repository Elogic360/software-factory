# Email System Critical Fixes — Implementation Spec

**Date:** 2026-07-13
**Status:** PLANNING
**Priority:** CRITICAL

---

## Problem Statement

The Integral Market organization email system has 3 critical bugs that prevent users from logging into their `@integralmarket.tech` email accounts via Bulwark (mail.integralmarket.tech) or Stalwart (imail.integralmarket.tech).

---

## Root Causes

### Bug 1: Stalwart Account Password Never Set
**File:** `integral-mail-backend/app/services/stalwart_client.py:112-176`

The `create_account()` method accepts `email` and `display_name` but NOT `password`. When admin grants an org email:
1. `admin_mail.py` generates `temp_password` via `secrets.token_urlsafe(16)`
2. Calls `stalwart.create_account(email, display_name)` — password NOT passed
3. Returns `temp_password` to admin UI
4. **User receives password that doesn't match Stalwart account → CANNOT LOGIN**

### Bug 2: Suspend/Reinstate Mismatch
**File:** `app/src/modules/admin/pages/AdminEmailPage.tsx:370-372`

Frontend sends `{ email: m.email }` but backend expects `{ mailbox_id: str }`:
- `SuspendMailboxRequest` has field `mailbox_id: str`
- `ReinstateMailboxRequest` has field `mailbox_id: str`
- Frontend sends `email` instead → Backend lookup fails silently

### Bug 3: MAILBOX_GRANT Event Never Published
**File:** `integral-mail-backend/app/api/v1/endpoints/admin_mail.py`

After successful grant, no event is published to Redis Stream. The `mail_event_handler.py` has a `_handle_mailbox_grant` handler that would:
- Send acceptance email to user's personal_email
- Log the grant event
- Notify admins

But it never fires because `publish_mailbox_grant()` is never called.

---

## Implementation Plan

### Phase 1: Fix Stalwart Password (Bug 1)

**Step 1.1: Update `stalwart_client.py`**

```python
# Current signature:
async def create_account(self, email: str, display_name: str) -> dict:

# New signature:
async def create_account(self, email: str, display_name: str, password: str = None) -> dict:
```

Inside `create_account()`, after creating the principal via JMAP:
- If `password` is provided, set it via Stalwart API or CLI
- Stalwart v0.16.x JMAP `Principal/set` may not support password setting
- **Fallback:** Use Stalwart CLI via SSH: `stalwart-cli -u http://localhost:8080 -c <password> account set password <email> <new_password>`

**Step 1.2: Update `admin_mail.py` grant endpoint**

Pass `temp_password` to `create_account()`:
```python
result = await stalwart.create_account(
    email=data.email,
    display_name=data.display_name,
    password=temp_password  # NEW
)
```

**Step 1.3: Add password to provisioning_service.py**

The event-driven provisioning path also needs password support:
- When auto-provisioning from USER_REGISTERED event, generate a random password
- Store it securely or send it to user's personal_email

### Phase 2: Fix Suspend/Reinstate (Bug 2)

**Step 2.1: Update `AdminEmailPage.tsx`**

Change lines 370-372 from:
```typescript
onClick={() => handleSuspend(m.email)}
// and
onClick={() => handleReinstate(m.email)}
```

To:
```typescript
onClick={() => handleSuspend(m.id)}
// and
onClick={() => handleReinstate(m.id)}
```

**Step 2.2: Verify `handleSuspend` and `handleReinstate` functions**

Ensure they send `{ mailbox_id: id }` in the request body.

### Phase 3: Wire MAILBOX_GRANT Event (Bug 3)

**Step 3.1: Add event publishing to `admin_mail.py`**

After successful grant:
```python
from app.services.event_bus import publish_mailbox_grant

await publish_mailbox_grant(
    user_id=str(data.user_id),
    email=data.email,
    display_name=data.display_name,
    granted_by=str(current_user.id)
)
```

**Step 3.2: Verify event handler in `mail_event_handler.py`**

Ensure `_handle_mailbox_grant()`:
- Sends acceptance email to user's `personal_email`
- Includes temp_password and acceptance_url
- Logs the grant event

### Phase 4: Send Acceptance Email

**Step 4.1: Update `admin_mail.py` to send acceptance email**

After grant, send email to user's personal email:
```python
await mail_client.send_email(
    to=data.personal_email,  # User's personal email
    subject="Your Integral Market Organization Email",
    template="org_email_grant",
    context={
        "email": data.email,
        "temp_password": temp_password,
        "acceptance_url": f"https://integralmarket.tech/accept-email/{acceptance_token}",
        "display_name": data.display_name
    }
)
```

---

## Database Changes

**None required.** The existing `mailboxes` table has all needed fields:
- `provisioning_status` (tracks grant state)
- `acceptance_token` (for user acceptance flow)
- `personal_email` (where to send grant notification)

---

## Testing Plan

### Unit Tests
1. Test `stalwart_client.create_account()` with password parameter
2. Test `admin_mail.py` grant endpoint returns password that works in Stalwart
3. Test suspend/reinstate sends correct `mailbox_id`

### Integration Tests
1. Full grant flow: Admin selects user → grants email → user can login to Bulwark
2. Suspend flow: Admin suspends → user cannot login → Admin reinstates → user can login
3. Event flow: Grant publishes event → acceptance email sent to personal_email

### Manual Verification
1. Login to `mail.integralmarket.tech` with granted credentials
2. Login to `imail.integralmarket.tech` admin with granted credentials
3. Send/receive test email

---

## Files to Modify

| File | Change |
|------|--------|
| `integral-mail-backend/app/services/stalwart_client.py` | Add `password` param to `create_account()` |
| `integral-mail-backend/app/api/v1/endpoints/admin_mail.py` | Pass password, publish event, send acceptance email |
| `integral-mail-backend/app/services/provisioning_service.py` | Add password support for event-driven path |
| `app/src/modules/admin/pages/AdminEmailPage.tsx` | Fix suspend/reinstate to use `m.id` |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Stalwart CLI not accessible from mail backend | Use JMAP `Principal/set` if supported, or SSH to Stalwart VPS |
| Password transmitted in plaintext | Use HTTPS for acceptance URL, temp password shown once only |
| Event handler fails silently | Add error logging and retry mechanism |

---

## Success Criteria

1. ✅ Admin can grant org email and user can login to Bulwark with temp_password
2. ✅ Admin can suspend/reinstate emails from UI without errors
3. ✅ Acceptance email sent to user's personal email after grant
4. ✅ All email delivery paths work (Brevo SMTP, Stalwart SMTP)
