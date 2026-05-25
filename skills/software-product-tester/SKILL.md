# SKILL: Software & Product Tester
## Domain: End-to-End Quality Engineering — UI, API, DB, Regression, Accessibility

**Activation triggers:** product testing, software testing, QA, test plan, regression test,
bug report, bug reproduction, acceptance test, UAT, UI test, browser test, API test,
integration test, smoke test, accessibility, a11y, WCAG, cross-browser, visual regression,
test coverage, test suite, playwright, pytest, locust, load test, performance test,
test automation, test the feature, write tests, verify this works.

---

## What This Skill Does

The Software & Product Tester is the **quality gate** across all four layers of the
Integral Market stack:

```
Browser / UI        → Playwright E2E, visual regression, accessibility
API Contract        → pytest + httpx integration tests
Database            → schema validation, data integrity assertions
Performance / Load  → Locust 10k user simulations
```

---

## Test Pyramid

```
         ╔══════════╗
         ║   E2E    ║   5–10% of tests  (slowest, highest confidence)
         ╚══════════╝
       ╔══════════════╗
       ║ Integration  ║  25–35%  (API + DB — real requests)
       ╚══════════════╝
     ╔══════════════════╗
     ║    Unit Tests    ║  55–70%  (fast, isolated, pure logic)
     ╚══════════════════╝
```

Never invert the pyramid. Never skip the middle layer.

---

## Layer 1 — Unit Tests (Python)

```bash
# Run all unit tests — zero dependencies on DB or external services
cd integral-expert-backend && source venv/bin/activate
pytest tests/unit/ -v --tb=short --cov=app --cov-report=term-missing

# Market backend
cd integral-market-backend && source venv/bin/activate
pytest tests/unit/ -v --tb=short

# Coverage gate: ≥ 80% on business logic modules
pytest tests/unit/ --cov=app/services --cov-fail-under=80
```

**What to unit-test:**
- Service layer functions (pure logic, no DB)
- Utility functions, validators, calculators
- Pydantic schema validation edge cases
- Risk engine formulas (copy trading, journal P&L)

**Template — FastAPI service unit test:**
```python
# tests/unit/test_journal_service.py
import pytest
from app.services.journal_service import calculate_pnl

def test_calculate_pnl_long_profit():
    result = calculate_pnl(entry=1.1000, exit=1.1050, size=1.0, direction="long")
    assert abs(result - 50.0) < 0.01

def test_calculate_pnl_short_loss():
    result = calculate_pnl(entry=1.1000, exit=1.1050, size=1.0, direction="short")
    assert abs(result - (-50.0)) < 0.01
```

---

## Layer 2 — Integration Tests (API + DB)

```bash
# Run integration tests (requires running PostgreSQL + Redis)
cd integral-expert-backend && source venv/bin/activate
pytest tests/integration/ -v --tb=short -x   # -x = stop on first failure

# Run only a specific domain
pytest tests/integration/test_journal_api.py -v
pytest tests/integration/test_copy_trading.py -v
```

**Template — FastAPI integration test with real DB:**
```python
# tests/integration/test_broker_accounts.py
import pytest
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

BASE = "http://localhost:8002"

@pytest.mark.asyncio
async def test_list_broker_accounts_requires_auth():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE}/api/v1/brokers/accounts")
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_list_broker_accounts_authenticated(auth_headers):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE}/api/v1/brokers/accounts",
            headers=auth_headers
        )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
```

**conftest.py fixture pattern:**
```python
# tests/conftest.py
import pytest
import httpx

@pytest.fixture
async def auth_headers():
    """Log in as test user and return Authorization header."""
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/api/v1/auth/login", json={
            "email": "testuser@integral.test",
            "password": "TestPass123!"
        })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

---

## Layer 3 — E2E Tests (Playwright / Browser)

```bash
# Install Playwright (once)
cd app && pnpm add -D @playwright/test && pnpm exec playwright install chromium

# Run E2E tests (all services must be running)
pnpm test:e2e
# OR:
npx playwright test --reporter=html

# Run single test file
npx playwright test e2e/auth.spec.ts --headed

# Debug mode (pause on failures)
npx playwright test --debug
```

**Template — Login E2E test:**
```typescript
// app/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('user can log in with valid credentials', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.fill('[data-testid="email-input"]', 'test@integral.test');
    await page.fill('[data-testid="password-input"]', 'TestPass123!');
    await page.click('[data-testid="login-button"]');
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 5000 });
    await expect(page.locator('[data-testid="user-avatar"]')).toBeVisible();
  });

  test('invalid credentials show error message', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    await page.fill('[data-testid="email-input"]', 'bad@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpass');
    await page.click('[data-testid="login-button"]');
    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      /invalid credentials/i
    );
  });

  test('Google OAuth button navigates to Google', async ({ page }) => {
    await page.goto('http://localhost:5173/login');
    const [popup] = await Promise.all([
      page.waitForEvent('popup'),
      page.click('[data-testid="google-oauth-button"]'),
    ]);
    await expect(popup).toHaveURL(/accounts\.google\.com/);
  });
});
```

**Template — Trading Journal E2E:**
```typescript
// app/e2e/journal.spec.ts
import { test, expect } from '@playwright/test';

test('trade list loads and shows entries', async ({ page }) => {
  // Assumes user is logged in (use storageState for auth reuse)
  await page.goto('http://localhost:5173/expert/journal');
  await expect(page.locator('[data-testid="trade-row"]').first()).toBeVisible({ timeout: 10000 });
  const count = await page.locator('[data-testid="trade-row"]').count();
  expect(count).toBeGreaterThan(0);
});
```

**playwright.config.ts:**
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  retries: 1,
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

---

## Layer 4 — Load Testing (Locust)

```bash
pip install locust
cd integral-expert-backend && source venv/bin/activate

# Run 50 users, spawn 5/s, for 60s (headless)
locust -f tests/load/locustfile.py \
  --host=http://localhost:8002 \
  --users=50 --spawn-rate=5 \
  --run-time=60s --headless

# MT5 broker sync load test (10k users simulation)
locust -f tests/load/locustfile_mt5.py \
  --host=http://localhost:8002 \
  --users=200 --spawn-rate=20 \
  --run-time=120s --headless
```

**Template — Locust load test:**
```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class JournalUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Log in and store token."""
        resp = self.client.post("/api/v1/auth/login", json={
            "email": "loadtest@integral.test",
            "password": "LoadTest123!"
        })
        self.token = resp.json().get("access_token", "")
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    @task(3)
    def list_trades(self):
        self.client.get("/api/v1/journal/trades?limit=20")

    @task(2)
    def get_equity_curve(self):
        self.client.get("/api/v1/journal/equity-curve?period=30d")

    @task(1)
    def get_analytics(self):
        self.client.get("/api/v1/journal/analytics")
```

**SLA targets (block merging if violated):**
```
P50 response time < 100ms  (journal reads)
P95 response time < 500ms
P99 response time < 2000ms
Error rate       < 0.1%
Throughput       > 1000 rps at 10k concurrent users (MT5 sync)
```

---

## Accessibility Testing

```bash
# Install axe-playwright
pnpm add -D @axe-core/playwright

# Run accessibility scan
npx playwright test e2e/accessibility.spec.ts
```

```typescript
// e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('Login page passes WCAG 2.1 AA', async ({ page }) => {
  await page.goto('/login');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});

test('Dashboard passes WCAG 2.1 AA', async ({ page }) => {
  await page.goto('/dashboard');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  // Log violations for dev awareness
  if (results.violations.length > 0) {
    console.log('A11y violations:', JSON.stringify(results.violations, null, 2));
  }
  expect(results.violations).toEqual([]);
});
```

---

## Bug Report Template

When a bug is found, file it using this template in `software-factory/memory/bugs/`:

```markdown
## BUG: <short title>  [YYYY-MM-DD]

**Severity:** Critical / High / Medium / Low
**Affected:** [Market :8000 | Expert :8002 | IMI :8003 | Frontend]
**Route / URL:** POST /api/v1/auth/oauth/google

### Steps to Reproduce
1. Navigate to /login
2. Click Google OAuth
3. Complete Google sign-in
4. Observe HTTP 500

### Expected
User is logged in and redirected to /dashboard

### Actual
HTTP 500 {"detail": "Internal server error"}

### Root Cause
ValueError in create_oauth_user() — no 'free' role in iam.roles table

### Fix
Three-layer: role fallback in auth_service.py + try/except in route + global handler
Commit: <git hash>

### Regression Test Added
tests/integration/test_oauth.py::test_google_oauth_with_missing_role
```

---

## Smoke Test Checklist (Run Before Every Deploy)

```bash
#!/bin/bash
# smoke_test.sh
set -e

echo "=== Smoke Test Suite ==="

# Auth
curl -sf http://localhost:8000/health > /dev/null && echo "✅ Market health"
curl -sf http://localhost:8002/health > /dev/null && echo "✅ Expert health"
curl -sf http://localhost:8003/health > /dev/null && echo "✅ IMI health"
curl -sf http://localhost:5173 > /dev/null && echo "✅ Frontend loads"

# API contracts
curl -sf http://localhost:8000/api/v1/auth/me -o /dev/null -w "Auth me: %{http_code}\n"
curl -sf http://localhost:8002/api/v1/journal/trades -o /dev/null -w "Journal: %{http_code}\n"
curl -sf http://localhost:8003/api/v1/intelligence/ -o /dev/null -w "IMI: %{http_code}\n"

echo "=== Smoke Test PASSED ==="
```

---

## Test Data Management

```python
# scripts/seed_test_data.py
"""
Run before integration / E2E tests to ensure clean, reproducible test data.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

TEST_USER = {
    "email": "testuser@integral.test",
    "password_hash": "<bcrypt of 'TestPass123!'>",
    "role": "user",
}

async def seed():
    engine = create_async_engine(os.environ["DATABASE_URL"])
    async with AsyncSession(engine) as db:
        # Clean up previous test data
        await db.execute(text("DELETE FROM iam.users WHERE email LIKE '%@integral.test'"))
        # Insert test user
        await db.execute(text("""
            INSERT INTO iam.users (email, hashed_password, is_active)
            VALUES (:email, :password_hash, true)
        """), TEST_USER)
        await db.commit()
    print("✅ Test data seeded")

asyncio.run(seed())
```

---

## Anti-Patterns

```
✗ Writing tests after the bug is fixed in production (too late)
✗ Testing only the happy path (missing edge cases)
✗ Skipping auth in integration tests (false green)
✗ Running E2E against production DB (data corruption)
✗ Not resetting test data between test runs (flaky tests)
✗ Measuring load test P50 only (hides tail latency)
✗ Ignoring a11y violations ("we'll fix it later")
✗ Committing with failing tests (CI must block merge)
```
