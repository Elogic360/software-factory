# SKILL: Testing Engineer
## Domain: Pytest (API), Playwright (E2E), Load Testing (Locust), Coverage

**Activation triggers:** test writing, API test, end-to-end test, load test,
test fixture, mock, factory pattern, coverage report, CI test pipeline.

---

## Test Architecture

```
tests/
  ├── conftest.py          ← shared fixtures: db, client, auth tokens
  ├── factories/           ← SQLAlchemy model factories (factory_boy)
  │   ├── user_factory.py
  │   ├── trade_factory.py
  │   └── broker_factory.py
  ├── unit/                ← pure logic, no DB
  │   ├── test_risk_engine.py
  │   └── test_analytics.py
  ├── integration/         ← DB-backed service tests
  │   ├── test_auth.py
  │   ├── test_broker_accounts.py
  │   └── test_journal.py
  └── e2e/                 ← Playwright browser tests
      ├── test_login.py
      ├── test_copy_trading.py
      └── test_journal_entry.py

e2e/                       ← Playwright root (separate from backend tests)
  ├── playwright.config.ts
  ├── fixtures/auth.ts
  └── tests/
      ├── auth.spec.ts
      └── journal.spec.ts
```

---

## Pytest Core Fixtures

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_async_db
from app.models import Base

TEST_DB_URL = "postgresql+asyncpg://test:test@localhost:5432/integral_test"

@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def db(engine):
    TestSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with TestSession() as session:
        yield session
        await session.rollback()    # rollback after each test — isolation guaranteed

@pytest_asyncio.fixture
async def client(db):
    def override_db():
        yield db
    app.dependency_overrides[get_async_db] = override_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def auth_headers(client, db):
    """Create user + return JWT bearer headers."""
    resp = await client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "full_name": "Test User",
    })
    assert resp.status_code == 201
    login = await client.post("/api/v1/auth/login", data={
        "username": "testuser@example.com",
        "password": "TestPass123!",
    })
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

---

## Factory Pattern (factory_boy)

```python
# tests/factories/trade_factory.py
import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models.journal import Trade
from decimal import Decimal
import uuid

class TradeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Trade
        sqlalchemy_session_persistence = "flush"

    id = factory.LazyFunction(uuid.uuid4)
    account_id = factory.LazyFunction(uuid.uuid4)
    ticket = factory.Sequence(lambda n: 1000000 + n)
    symbol = "EURUSD"
    direction = "buy"
    volume = Decimal("0.10")
    open_price = Decimal("1.08500")
    close_price = Decimal("1.09000")
    profit = Decimal("50.00")
    status = "closed"
    opened_at = factory.LazyFunction(lambda: datetime.utcnow() - timedelta(hours=2))
    closed_at = factory.LazyFunction(datetime.utcnow)
```

---

## API Integration Tests

```python
# tests/integration/test_journal.py
import pytest

@pytest.mark.asyncio
async def test_get_trade_history_requires_auth(client):
    resp = await client.get("/api/v1/journal/trades")
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_get_trade_history_returns_trades(client, auth_headers, db):
    # Create 3 trades for this user's account
    account = await BrokerAccountFactory.create(session=db)
    trades = await TradeFactory.create_batch(3, session=db, account_id=account.id)

    resp = await client.get(f"/api/v1/journal/trades?account_id={account.id}", headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 3
    assert data["total"] == 3

@pytest.mark.asyncio
async def test_performance_summary_win_rate(client, auth_headers, db):
    account = await BrokerAccountFactory.create(session=db)
    # 7 wins, 3 losses
    await TradeFactory.create_batch(7, session=db, account_id=account.id, profit=Decimal("100"))
    await TradeFactory.create_batch(3, session=db, account_id=account.id, profit=Decimal("-50"))

    resp = await client.get(
        f"/api/v1/journal/performance?account_id={account.id}",
        headers=auth_headers,
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["win_rate"] == pytest.approx(0.7, abs=0.01)
    assert body["total_trades"] == 10
    assert float(body["total_pnl"]) == pytest.approx(550.0)
```

---

## Risk Engine Unit Tests

```python
# tests/unit/test_risk_engine.py
import pytest
from app.services.copy_trading.risk_engine import RiskEngine

@pytest.mark.asyncio
async def test_risk_engine_blocks_on_drawdown():
    engine = RiskEngine()
    subscription = MagicMock()
    subscription.max_drawdown_pct = 0.10
    subscription.daily_loss_limit = None
    subscription.max_lot_size = None
    subscription.allowed_symbols = None

    signal = MagicMock(lot_size=1.0, symbol="EURUSD")

    with patch.object(engine, '_current_drawdown', return_value=0.15):
        allowed, reason = await engine.check_limits(subscription, signal)

    assert not allowed
    assert "drawdown" in reason.lower()

@pytest.mark.asyncio
async def test_risk_engine_allows_valid_signal():
    engine = RiskEngine()
    subscription = MagicMock()
    subscription.max_drawdown_pct = 0.20
    subscription.daily_loss_limit = 500
    subscription.max_lot_size = 2.0
    subscription.allowed_symbols = ["EURUSD", "GBPUSD"]
    subscription.copy_ratio = 1.0

    signal = MagicMock(lot_size=0.5, symbol="EURUSD")

    with patch.object(engine, '_current_drawdown', return_value=0.05):
        with patch.object(engine, '_daily_loss', return_value=100):
            allowed, reason = await engine.check_limits(subscription, signal)

    assert allowed
    assert reason == ""
```

---

## Playwright E2E Tests

```typescript
// e2e/tests/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('user can login with email and password', async ({ page }) => {
    await page.goto('/auth/login');

    await page.fill('[data-testid="email-input"]', 'testuser@integralmarket.com');
    await page.fill('[data-testid="password-input"]', 'TestPass123!');
    await page.click('[data-testid="login-button"]');

    await expect(page).toHaveURL('/expert/charts', { timeout: 10_000 });
    await expect(page.locator('[data-testid="account-menu"]')).toBeVisible();
  });

  test('invalid credentials show error', async ({ page }) => {
    await page.goto('/auth/login');
    await page.fill('[data-testid="email-input"]', 'wrong@example.com');
    await page.fill('[data-testid="password-input"]', 'wrongpass');
    await page.click('[data-testid="login-button"]');

    await expect(page.locator('[data-testid="error-message"]')).toContainText('Invalid');
  });
});
```

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e/tests',
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Load Testing (Locust)

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class TradingUser(HttpUser):
    wait_time = between(1, 3)
    token: str = ""

    def on_start(self):
        resp = self.client.post("/api/v1/auth/login", data={
            "username": "loadtest@integralmarket.com",
            "password": "LoadTest123!",
        })
        self.token = resp.json()["access_token"]

    @task(3)
    def get_positions(self):
        self.client.get(
            "/api/v1/brokers/accounts/test-account-id/positions",
            headers={"Authorization": f"Bearer {self.token}"},
        )

    @task(2)
    def get_trade_history(self):
        self.client.get(
            "/api/v1/journal/trades?account_id=test-account-id&limit=50",
            headers={"Authorization": f"Bearer {self.token}"},
        )

    @task(1)
    def get_performance(self):
        self.client.get(
            "/api/v1/journal/performance?account_id=test-account-id",
            headers={"Authorization": f"Bearer {self.token}"},
        )

# Run: locust -f tests/load/locustfile.py --host=http://localhost:8002 -u 100 -r 10
```

---

## Anti-Patterns

```
✗ Tests sharing DB state (no rollback → test pollution)
✗ Hardcoded UUIDs in tests (use factory_boy sequences)
✗ Testing implementation details (test behavior, not internals)
✗ No auth fixture (repeating login in every test)
✗ E2E tests with no data-testid attributes (brittle CSS selectors)
✗ Load test with real user credentials (use dedicated test accounts)
✗ Missing pytest.ini markers (slow/e2e should be excluded from unit runs)
✗ asserting exact strings on error messages (messages change, assert status codes)
```
