# UI/UX Design Brief: {{PRODUCT_TITLE}}

**Document ID:** BRF-{{PROJECT_ID}}-001  
**Version:** {{VERSION}}  
**Status:** {{STATUS}} (Draft | Under Review | Approved)  
**Parent PRD:** PRD-{{PROJECT_ID}}-001  
**Target Specification:** {{TARGET_SPEC_ID}}  
**Design Lead:** {{DESIGN_LEAD}}  
**Last Updated:** {{DATE}}  

---

## 1. Executive Purpose & Design Scope

The purpose of this Design Brief is to establish high-level aesthetic, behavioral, and accessibility parameters for {{PRODUCT_TITLE}} to align engineering, product, and design stakeholders before detailed screen authoring begins.

---

## 2. Target Platforms & Display Environments

- [x] Modern Desktop Web (Chrome, Safari, Firefox, Edge)
- [x] Responsive Mobile Web (iOS Safari, Android Chrome)
- [ ] Native Mobile (iOS Swift / Android Kotlin)
- [ ] Embedded / PWA

---

## 3. Brand Personality, Tone & Aesthetic Principles

- **Tone & Voice:** {{BRAND_TONE}} (e.g., Ultra-crisp, high-density, authoritative, zero-clutter)
- **Key Differentiators:**
  1. {{DIFFERENTIATOR_1}}
  2. {{DIFFERENTIATOR_2}}
- **Visual Mood:** Modern institutional dark-mode, high-contrast data visualization, strict typographic rhythm.

---

## 4. Primary User Goals by Core Screen

| Screen ID | Screen Name | Primary User Goal | Key Information Displayed |
|-----------|-------------|-------------------|--------------------------|
| SCR-01 | Login Screen | Rapid authentication into workspace | Credential inputs, SSO options |
| SCR-02 | Main Dashboard | Real-time situation awareness & navigation | System metrics, active resources, alerts |
| SCR-03 | Resource Detail | Deep inspection & parameter configuration | Tabbed telemetry, audit history, action controls |
| SCR-04 | Resource Creator | Error-free entity creation & preview | Validated inputs, step wizard, preview panel |

---

## 5. Responsive Breakpoint Matrix

| Viewport Category | Breakpoint Range | Layout Behavior | Target Devices |
|-------------------|------------------|-----------------|----------------|
| **Mobile (Compact)** | `320px - 639px` | Single column vertical stack, bottom navigation bar, collapsible drawers | Smartphones |
| **Tablet (Medium)** | `640px - 1023px` | Two-column grid, compact sidebar, modal dialogs | iPads, Tablets |
| **Desktop (Expanded)** | `1024px - 1439px` | Multi-panel workspace, fixed left navigation, data tables | Standard Laptops / Monitors |
| **Wide / Ultrawide** | `1440px+` | Multi-column dashboard, dense real-time charts, side-by-side comparisons | Large Displays, Multi-monitors |

---

## 6. Accessibility & Compliance Bar

- **Standard:** WCAG 2.2 Level AA strict compliance across all components and viewports.
- **Color Contrast:** Minimum 4.5:1 for normal text, 3:0:1 for large text and UI components.
- **Keyboard Navigation:** 100% accessible via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Escape`, arrow keys).
- **Screen Reader Support:** Semantic HTML elements with complete ARIA roles, states, and live regions.

---

## 7. Signoff

- [ ] Stakeholder alignment achieved
- [ ] Approved to proceed to Full UI/UX Specification: {{APPROVER}} on {{SIGNOFF_DATE}}
