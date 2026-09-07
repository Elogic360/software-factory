# Full UI/UX Specification: QuantumVault Ledger Engine

**Document ID:** UIX-QV-001  
**Version:** 1.0.0  
**Status:** Approved  
**Parent Brief:** BRF-QV-001  
**Parent App Flow:** FLW-QV-001  
**Target Specification:** SPEC-QUANTUM-VAULT-2026  
**Lead UI/UX Architect:** Principal UI/UX Architect  
**Last Updated:** 2026-09-07  

---

## 1. Design System & Token Foundation

### 1.1 Color Tokens (Semantic Palette)
```yaml
colors:
  bg:
    base: "#0B0E14"
    surface: "#151922"
    overlay: "#1E2430"
  text:
    primary: "#F8FAFC"
    secondary: "#94A3B8"
    muted: "#64748B"
  accent:
    primary: "#06B6D4"
    primary_hover: "#0891B2"
  state:
    success: "#10B981"
    warning: "#F59E0B"
    danger: "#EF4444"
    info: "#3B82F6"
  border:
    subtle: "#1E293B"
    strong: "#334155"
```

### 1.2 Typography Tokens
- **Font Families:** UI: `Inter, sans-serif`; Numbers/Data: `JetBrains Mono, monospace`
- **Scale:**
  - H1 Display: `32px` (Line: 40px, Weight: 700)
  - H2 Section: `24px` (Line: 32px, Weight: 600)
  - Body Large: `16px` (Line: 24px, Weight: 400)
  - Body Regular: `14px` (Line: 20px, Weight: 400)
  - Micro / Tag: `12px` (Line: 16px, Weight: 500)

### 1.3 Spacing & Elevation
- **Spacing Scale:** `4px`, `8px`, `16px`, `24px`, `32px`, `48px`
- **Border Radius:** `4px` (badges), `8px` (inputs/buttons), `12px` (cards/panels)
- **Shadows:** `elevation-1` (0 1px 3px rgba(0,0,0,0.5)), `elevation-2` (0 8px 16px rgba(0,0,0,0.6))

---

## 2. Reusable Component Inventory

| Component Name | Category | Primary Props & States | Accessibility & ARIA Notes |
|----------------|----------|------------------------|-----------------------------|
| `AppNavbar` | Navigation | items, activeItem, userProfile | `<nav aria-label="Main Navigation">`, skip link |
| `DataTable` | Data Display | columns, data, sortKey, onSort, page | `<table aria-describedby="...">`, keyboard header sort |
| `ActionButton` | Input / Control | variant (primary/danger), loading, disabled | `<button aria-busy="...">`, visible focus ring |
| `InputFormField`| Form Element | label, value, error, placeholder, helpText | `<label for="...">`, `<input aria-invalid="...">` |
| `ModalDialog` | Feedback / Overlay | isOpen, title, onClose, children | `<div role="dialog" aria-modal="true">`, focus trap |
| `StatusBadge` | Status | status (success/warning/danger), text | `<span role="status">` |
| `EmptyStateCard`| Feedback | icon, title, description, actionButton | Accessible icon with descriptive text |

---

## 3. Per-Screen Specifications

### 3.1 Screen SCR-01: Vault Authentication
- **App Flow Reference:** `SCR-01` in `FLW-QV-001`
- **Purpose:** Secure authentication into treasury operations console.
- **Layout:** Centered card (max-width: 440px) on `#0B0E14` base background.
- **Component Breakdown:** Brand header, `InputFormField` for identity token, submit `ActionButton`.
- **State Matrix:**
  - *Default State:* Empty inputs, cursor auto-focused on identity field.
  - *Loading State:* Submit button enters spinner state; inputs disabled.
  - *Empty State:* Initial state with clear helper prompt.
  - *Error State:* Red alert banner "Invalid credentials or expired session" (`aria-live="polite"`).
  - *Success State:* Green checkmark transition and immediate redirect to `/dashboard`.
- **Responsive Behavior:** 100% width on Mobile; centered 440px on Desktop.
- **Accessibility:** Tab order: Token Input -> Remember Session -> Submit.

### 3.2 Screen SCR-02: Ledger Dashboard
- **App Flow Reference:** `SCR-02` in `FLW-QV-001`
- **Purpose:** Primary command center displaying live account liquidity and streaming transactions.
- **Layout:** Left persistent sidebar, top metric strip, main `DataTable`.
- **Component Breakdown:** `AppNavbar`, metrics cards, `DataTable` for transactions, `StatusBadge`.
- **State Matrix:**
  - *Default State:* Populated data table with active WebSocket sync indicator.
  - *Loading State:* Shimmer skeleton loaders across metrics cards and table rows.
  - *Empty State:* `EmptyStateCard` with "No transactions recorded yet" and "Initiate Transfer" button.
  - *Error State:* Top banner alert "Real-time sync interrupted. Retrying in 5s..." with retry button.
  - *Success State:* Pulse emerald animation on newly arrived streaming transactions.
- **Responsive Behavior:** On Mobile, sidebar collapses into bottom drawer; table scrolls horizontally.
- **Accessibility:** Data rows announce status changes through `aria-live="polite"`.

### 3.3 Screen SCR-03: Transaction Detail
- **App Flow Reference:** `SCR-03` in `FLW-QV-001`
- **Purpose:** Granular inspection of double-entry ledger journals and cryptographic receipts.
- **Layout:** Split view: left summary card, right debit/credit journal table.
- **Component Breakdown:** Journal line item table, hash proof badge, print receipt button.
- **State Matrix:**
  - *Default State:* Full transaction metadata and balanced debit/credit lines.
  - *Loading State:* Centered pulse loader with "Retrieving ledger verification...".
  - *Empty State:* "Transaction not found" card with back to dashboard link.
  - *Error State:* "Failed to load audit receipt" banner with retry button.
  - *Success State:* Verified cryptographic signature badge displayed in emerald.
- **Responsive Behavior:** Stacks vertically on Mobile; side-by-side on Desktop.
- **Accessibility:** Visual debit (red) and credit (green) indicators supplemented with text prefix ("DR" / "CR").

### 3.4 Screen SCR-04: Transfer Execution Wizard
- **App Flow Reference:** `SCR-04` in `FLW-QV-001`
- **Purpose:** Step-by-step form to construct, validate, and execute double-entry settlements.
- **Layout:** Centered multi-step form panel with real-time balance impact preview.
- **Component Breakdown:** Source account picker, target account input, currency dropdown, amount input, idempotency key generator.
- **State Matrix:**
  - *Default State:* Active form fields with auto-generated client UUID idempotency key.
  - *Loading State:* "Broadcasting settlement to ledger..." modal overlay with progress bar.
  - *Empty State:* N/A (form wizard).
  - *Error State:* Inline field validation errors (e.g. "Amount exceeds available balance").
  - *Success State:* Modal transitions to success state and forwards to `SCR-03`.
- **Responsive Behavior:** Full width single column on all mobile screens.
- **Accessibility:** Escape key cancels modal; tab focus trapped inside modal while open.

---

## 4. Microcopy & Validation Rules

| Field / Action | Validation Rule | Error Microcopy | Helper Text |
|----------------|-----------------|-----------------|-------------|
| Account Number | 10-20 alphanumeric characters | "Account number must be 10-20 alphanumeric characters." | "Enter recipient treasury ledger account." |
| Transfer Amount| Numeric > 0.00, <= available balance | "Amount must be greater than 0 and not exceed balance." | "Specified in account base currency." |
| Idempotency Key| Valid UUID v4 string | "Invalid idempotency key format." | "Unique identifier preventing duplicate execution." |

---

## 5. Traceability & Gate Signoff

- [x] All screens from `FLW-QV-001` defined with complete 5-state matrices (0 orphan screens)
- [x] WCAG 2.2 Level AA compliance verified for all primitives
- [x] Responsive behavior specified for all 4 breakpoint bands
- [x] Approved for Production Station Entry by Principal UI/UX Architect on 2026-09-07
