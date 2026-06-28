
## 2026-06-01 — Session 2 UI Renovations

### Pages renovated
- user/DashboardPage.tsx (929 lines) — hero + market ticker + KPI + XP bar
- user/ProfilePage.tsx (978 lines) — 3 tabs (Personal/Security/Preferences)
- user/SettingsPage.tsx (981 lines) — 5 sections (Notifications/Privacy/Security/Display/Danger)
- admin/AdminDashboard.tsx (781 lines) — 6 KPIs, role distribution, system status
- admin/AdminProfilePage.tsx (947 lines) — Power Level animated bar, role hierarchy
- admin/AdminSettingsPage.tsx (776 lines) — platform settings with toast notifications
- community/BlogPage.tsx — premium featured post hero, category tabs, debounced search, Load More
- community/BlogPostPage.tsx — read progress bar, sticky share sidebar, related articles
- community/WebinarsPage.tsx — "Webinars & Events", event type badges, WhatsApp display
- admin/AdminWebinars.tsx — External Participants tab, event type support
- webinars/WebinarDetailPage.tsx — event_type badge, location, WhatsApp group link

### API endpoint fixes (critical)
- AdminCourses: /admin/courses → /academy/admin/courses (create/list/delete/publish)
- AdminCourses: update via PUT /api/v1/courses/{id}
- AdminCourses: requires instructor_id = current user.id on create
- AdminLibrary GET: /library/admin → /library/documents
- AdminLibrary mutations: /library/admin/{id} → /library/admin/documents/{id}

### New backend endpoints added to integral-market-backend
- POST /api/v1/library/admin/documents — JSON URL-based document create (no file upload)
- PATCH /api/v1/library/admin/documents/{id}/access-type now accepts JSON body {access_type_id, price, is_published}

### Logo
- Both Header.tsx and AdminLayout.tsx: h-11/h-12, rounded-2xl, padding 3px
