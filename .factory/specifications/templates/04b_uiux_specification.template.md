# Full UI/UX Specification: {{PRODUCT_TITLE}}

**Document ID:** UIX-{{PROJECT_ID}}-001  
**Version:** {{VERSION}}  
**Status:** {{STATUS}} (Draft | Approved | Implementation Ready)  
**Parent Brief:** BRF-{{PROJECT_ID}}-001  
**Parent App Flow:** FLW-{{PROJECT_ID}}-001  
**Target Specification:** {{TARGET_SPEC_ID}}  
**Lead UI/UX Architect:** {{LEAD_DESIGNER}}  
**Last Updated:** {{DATE}}  

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
    primary: "#3B82F6"
    primary_hover: "#2563EB"
  state:
    success: "#10B981"
    warning: "#F59E0B"
    danger: "#EF4444"
    info: "#06B6D4"
  border:
    subtle: "#1E293B"
    strong: "#334155"
```

### 1.2 Typography Tokens
- **Font Families:** Display/UI: `Inter, sans-serif`; Code/Data: `JetBrains Mono, monospace`
- **Scale:**
  - Heading 1: `32px` / Line Height: `40px` / Weight: `700`
  - Heading 2: `24px` / Line Height: `32px` / Weight: `600`
  - Body Large: `16px` / Line Height: `24px` / Weight: `400`
  - Body Base: `14px` / Line Height: `20px` / Weight: `400`
  - Caption / Micro: `12px` / Line Height: `16px` / Weight: `500`

### 1.3 Spacing & Elevation
- **Spacing Scale:** `4px` (xs), `8px` (sm), `16px` (md), `24px` (lg), `32px` (xl), `48px` (2xl)
- **Border Radius:** `4px` (input/tag), `8px` (card/button), `12px` (modal/panel)
- **Shadows/Elevation:** `elevation-1` (0 1px 3px rgba(0,0,0,0.4)), `elevation-2` (0 4px 6px rgba(0,0,0,0.5))

---

## 2. Reusable Component Inventory

| Component Name | Category | Primary Props & States | Accessibility & ARIA Notes |
|----------------|----------|------------------------|-----------------------------|
| `AppNavbar` | Navigation | items, activeItem, userProfile | `<nav aria-label="Main Navigation">`, skip link |
| `DataTable` | Data Display | columns, data, sortKey, onSort, page | `<table aria-describedby="...">`, keyboard header sort |
| `ActionButton` | Input / Control | variant (primary/danger), loading, disabled | `<button aria-busy="...">`, focus ring |
| `InputFormField`| Form Element | label, value, error, placeholder, helpText | `<label for="...">`, `<input aria-invalid="...">` |
| `ModalDialog` | Feedback / Overlay | isOpen, title, onClose, children | `<div role="dialog" aria-modal="true">`, focus trap |
| `StatusBadge` | Status | status (success/warning/danger), text | `<span role="status">` |
| `EmptyStateCard`| Feedback | icon, title, description, actionButton | Descriptive SVG with `aria-hidden="true"` |

---

## 3. Per-Screen Specifications

### 3.1 Screen SCR-01: {{SCREEN_01_NAME}}
- **App Flow Reference:** `SCR-01` in `FLW-{{PROJECT_ID}}-001`
- **Purpose:** {{SCREEN_01_PURPOSE}}
- **Layout & Component Breakdown:**
  - Central modal / container card (`elevation-2`).
  - Top: Brand logo and title.
  - Middle: `InputFormField` for identity / email and credentials.
  - Bottom: `ActionButton` (primary) + alternate SSO options.
- **State Matrix:**
  - *Default State:* Clean inputs with autofocus on first field.
  - *Loading State:* Submit button enters `loading=true`, spinner active, inputs disabled.
  - *Empty State:* N/A.
  - *Error State:* Inline field alert in red with error message, `aria-invalid="true"`.
  - *Success State:* Smooth transition redirect to `/dashboard`.
- **Responsive Behavior:**
  - Mobile: Full width card (padding: 16px).
  - Desktop: Centered card (max-width: 440px).
- **Accessibility & ARIA:**
  - Focus order: Email -> Password -> Remember Me -> Submit.
  - Error announcements via `aria-live="polite"`.

### 3.2 Screen SCR-02: {{SCREEN_02_NAME}}
- **App Flow Reference:** `SCR-02` in `FLW-{{PROJECT_ID}}-001`
- **Purpose:** Primary application control panel displaying telemetry and resource list.
- **Layout & Component Breakdown:**
  - Left: Fixed `AppNavbar`.
  - Top: Header bar with workspace switcher and user profile.
  - Main: Top metrics card row (`elevation-1`), followed by main `DataTable`.
- **State Matrix:**
  - *Default State:* Populated data table with pagination controls.
  - *Loading State:* Shimmer / skeleton loaders matching row dimensions.
  - *Empty State:* `EmptyStateCard` rendered with "No items created yet" and "Create Resource" button.
  - *Error State:* Error banner across top of table with "Retry Fetch" button.
  - *Success State:* Inline badge showing live sync status.
- **Responsive Behavior:**
  - Mobile: Sidebar collapses to hamburger menu; table scrolls horizontally with fixed first column.
  - Desktop: Full sidebar expanded, full grid.
- **Accessibility & ARIA:**
  - Table headers announce sort order (`aria-sort="ascending"`).

### 3.3 Screen SCR-03: {{SCREEN_03_NAME}}
- **App Flow Reference:** `SCR-03` in `FLW-{{PROJECT_ID}}-001`
- **Purpose:** Deep telemetry inspection and item actions.
- **Layout:** Two-column split layout (overview left, telemetry graph right).
- **States:** Loading spinner, error fallback banner, real-time update indicator.

### 3.4 Screen SCR-04: {{SCREEN_04_NAME}}
- **App Flow Reference:** `SCR-04` in `FLW-{{PROJECT_ID}}-001`
- **Purpose:** Guided creation form for new entity.
- **States:** Step validation, live preview, submission progress bar.

---

## 4. Microcopy & Validation Rules

| Field / Action | Validation Rule | Error Microcopy | Helper Text |
|----------------|-----------------|-----------------|-------------|
| Email / Identifier | Valid email format | "Please enter a valid email address." | "Use your organization email." |
| Resource Name | 3-50 chars, alphanumeric + hyphens | "Name must be 3-50 letters, numbers, or hyphens." | "Unique human-readable identifier." |
| Deletion Action | Explicit confirmation typing | "Type 'CONFIRM' to proceed with deletion." | "This operation is irreversible." |

---

## 5. Traceability & Gate Signoff

- [ ] All screens from `FLW-{{PROJECT_ID}}-001` defined with states (0 orphan screens)
- [ ] WCAG 2.2 Level AA compliance verified for all primitives
- [ ] Responsive behavior specified for all 4 breakpoint bands
- [ ] Approved for Production Station Entry: {{APPROVER}} on {{SIGNOFF_DATE}}
