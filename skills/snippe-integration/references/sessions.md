# Checkout Sessions & Payment Links

Sessions provide a **hosted checkout page** so you don't need to build your own payment form. Snippe handles the UI, method selection, and polling. This is the right choice when you want a pre-built, mobile-optimised checkout — especially when you want to share a payment URL via SMS, WhatsApp, email, or printed materials.

For full control over the UI (custom payment forms, embedded flows), use the Payments API instead — see `references/payments.md`.

## Table of contents

- [When to use sessions](#when-to-use-sessions)
- [Create a session](#create-a-session)
- [The two URLs: checkout_url vs payment_link_url](#the-two-urls-checkout_url-vs-payment_link_url)
- [Allowed payment methods](#allowed-payment-methods)
- [Custom amounts (donations, tips)](#custom-amounts-donations-tips)
- [Session status lifecycle](#session-status-lifecycle)
- [Endpoints](#endpoints)
- [Payment profiles](#payment-profiles)

## When to use sessions

Reach for sessions when **any** of these apply:

- You want a mobile-optimised checkout UI without building one yourself.
- You need a single URL that lets the customer pick between mobile money, card, and QR.
- You want to send a payment link over SMS / WhatsApp / email / print.
- You want Snippe to handle status polling for you so the user sees a spinner and a success page without you writing that code.

If you're building an embedded SDK, a native mobile app with a custom flow, or a headless POS, prefer the Payments API.

## Create a session

```http
POST /api/v1/sessions
Authorization: Bearer <api_key>
Content-Type: application/json
```

Note the `/api/v1` prefix — sessions live at a slightly different path than the Payments API (`/v1/payments`).

### Basic request

```json
{
  "amount": 50000,
  "currency": "TZS",
  "allowed_methods": ["mobile_money", "qr"],
  "customer": {
    "name": "John Doe",
    "phone": "+255712345678",
    "email": "john@example.com"
  },
  "redirect_url": "https://yoursite.com/success",
  "webhook_url": "https://yoursite.com/webhooks/snippe",
  "description": "Order #12345",
  "metadata": { "order_id": "12345" },
  "expires_in": 3600
}
```

### Response

```json
{
  "code": 201,
  "data": {
    "reference": "sess_abc123def456",
    "status": "pending",
    "amount": 50000,
    "currency": "TZS",
    "checkout_url": "https://snippe.me/checkout/W0SzdUSHQm",
    "short_code": "Ax7kM2",
    "payment_link_url": "https://snippe.me/p/Ax7kM2",
    "expires_at": "2026-02-26T11:00:00Z"
  }
}
```

Note the shape difference vs the Payments API: session responses put `amount` and `currency` as top-level scalars, not a nested `{value, currency}` object. Webhook payloads for session events still use the envelope/object format documented in `references/webhooks.md`.

## The two URLs: checkout_url vs payment_link_url

The response returns **two** URLs. They point to the same session but are used for different purposes:

| Field              | Example                              | Use when…                                                      |
| ------------------ | ------------------------------------ | -------------------------------------------------------------- |
| `checkout_url`     | `https://snippe.me/checkout/W0Szd…`  | Embedding the checkout in an app or opening it in a WebView    |
| `payment_link_url` | `https://snippe.me/p/Ax7kM2`         | Sharing via SMS, WhatsApp, email, QR on a poster, short links  |

Both resolve to the same checkout experience. `payment_link_url` is a short vanity URL built from `short_code` — it's easier to read aloud over the phone and fits in a single SMS. Prefer it for anything the end customer will see or type.

## Allowed payment methods

Restrict which methods appear on the checkout page with `allowed_methods`:

| Value          | Covers                                       |
| -------------- | -------------------------------------------- |
| `mobile_money` | Airtel Money, M-Pesa, Mixx by Yas, Halotel   |
| `qr`           | Dynamic QR for scan-to-pay                   |
| `card`         | Visa, Mastercard, local debit                |

Pass an array of one or more values. Omitting `allowed_methods` shows all enabled methods on the account. Useful patterns:

- **Mobile-money-only** for a USSD-heavy customer base: `["mobile_money"]`
- **Cardless checkout** for donations or small tips: `["mobile_money", "qr"]`
- **Card-only** for international-ish buyers: `["card"]`

## Custom amounts (donations, tips)

For flows where the customer picks the amount (donation pages, tip jars, pay-what-you-want), set `allow_custom_amount` instead of `amount`:

```json
{
  "allow_custom_amount": true,
  "min_amount": 1000,
  "max_amount": 500000,
  "description": "Donation"
}
```

The checkout page will show an amount input field between `min_amount` and `max_amount`. Both bounds are in TZS.

## Session status lifecycle

| Status      | Meaning                           |
| ----------- | --------------------------------- |
| `pending`   | Created, awaiting payment         |
| `active`    | Payment in progress               |
| `completed` | Payment successful                |
| `expired`   | Not paid before `expires_at`      |
| `cancelled` | Cancelled via the cancel endpoint |

`expires_in` (in seconds on create) controls how long a session stays valid. Default is 3600 (1 hour). After expiry the URLs return an error page to the customer.

## Endpoints

| Endpoint                              | Method | Description         |
| ------------------------------------- | ------ | ------------------- |
| `/api/v1/sessions`                    | POST   | Create session      |
| `/api/v1/sessions`                    | GET    | List sessions       |
| `/api/v1/sessions/{reference}`        | GET    | Get session details |
| `/api/v1/sessions/{reference}/cancel` | POST   | Cancel session      |

Cancellation is only valid for `pending` or `active` sessions — cancelling an already-`completed` session is a no-op.

## Payment profiles

Payment profiles store **reusable branding and defaults** — merchant name, logo, brand colour, locale, default URLs — so every session inherits the same look without you repeating it on each request. Create profiles in the Snippe Dashboard under **Settings → Payment Profiles**, then reference them by `profile_id`:

```json
{
  "profile_id": "prof_550e8400-e29b-41d4-a716-446655440000",
  "amount": 50000,
  "description": "Order #12345"
}
```

### What comes from the profile vs. the request

Some fields can **only** come from the profile (branding), while others can be set on the profile as a default and **overridden per request** (operational config):

| Field              | Source                                 |
| ------------------ | -------------------------------------- |
| `merchant_name`    | Profile only                           |
| `merchant_logo`    | Profile only                           |
| `brand_color`      | Profile only                           |
| `locale`           | Profile only                           |
| `collect_email`    | Profile only                           |
| `redirect_url`     | Profile default, overridable per request |
| `webhook_url`      | Profile default, overridable per request |
| `allowed_methods`  | Profile default, overridable per request |

If you want consistent branding across all sessions — which is usually what you want — create a profile once and just pass `profile_id` on each create call. Override `redirect_url`, `webhook_url`, and `allowed_methods` inline only when a specific session needs different behaviour (e.g. a campaign page with a unique thank-you URL).
