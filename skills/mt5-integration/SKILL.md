# SKILL: MT5 Integration Engineer
## Domain: MetaTrader 5, Broker Adapters, Trade Execution

**Activation triggers:** MT5 connection, trade sync, broker adapter, execution
gateway, position management, order placement.

---

## Broker Adapter Interface

```python
# integral-expert-backend/app/services/integrations/brokers/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

@dataclass
class AccountInfo:
    login: str
    name: str
    balance: Decimal
    equity: Decimal
    margin: Decimal
    free_margin: Decimal
    currency: str
    leverage: int
    is_live: bool

@dataclass
class Position:
    ticket: int
    symbol: str
    direction: str  # 'buy' | 'sell'
    volume: float
    open_price: float
    current_price: float
    pnl: float
    swap: float
    comment: str
    opened_at: str

class BrokerAdapterBase(ABC):
    @abstractmethod
    async def connect(self) -> bool: ...
    @abstractmethod
    async def disconnect(self) -> None: ...
    @abstractmethod
    async def get_account_info(self) -> AccountInfo: ...
    @abstractmethod
    async def get_open_positions(self) -> List[Position]: ...
    @abstractmethod
    async def get_trade_history(self, from_dt, to_dt) -> List[dict]: ...
    @abstractmethod
    async def place_order(self, symbol, direction, volume, price=None) -> dict: ...
    @abstractmethod
    async def close_position(self, ticket: int) -> bool: ...
```

---

## MT5 Sync Worker Pattern

```python
# Workers run on a schedule (APScheduler) — not in request path
# integral-expert-backend/app/workers/mt5_sync_worker.py

async def sync_account_trades(account_id: str, db: AsyncSession) -> None:
    """Sync MT5 trades to journal.trades table."""
    try:
        adapter = await BrokerRegistry.instance().get(account_id, db)
        history = await adapter.get_trade_history(
            from_dt=datetime.utcnow() - timedelta(days=7),
            to_dt=datetime.utcnow(),
        )
        for trade in history:
            await upsert_trade(db, account_id, trade)
        await db.commit()
        logger.info("Sync complete", extra={"account_id": account_id, "trades": len(history)})
    except Exception as exc:
        logger.error("Sync failed", extra={"account_id": account_id, "error": str(exc)})
        # Never raise — sync failures are logged, not propagated
```

---

## BrokerRegistry Singleton

```python
# integral-expert-backend/app/services/integrations/brokers/registry.py
class BrokerRegistry:
    _instance: Optional["BrokerRegistry"] = None
    _adapters: dict[str, BrokerAdapterBase] = {}

    @classmethod
    def instance(cls) -> "BrokerRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def get(self, account_id: str, db: AsyncSession, force_reconnect: bool = False) -> BrokerAdapterBase:
        if account_id in self._adapters and not force_reconnect:
            return self._adapters[account_id]
        adapter = await self._create_adapter(account_id, db)
        await adapter.connect()
        self._adapters[account_id] = adapter
        return adapter

    async def remove(self, account_id: str) -> None:
        if adapter := self._adapters.pop(account_id, None):
            await adapter.disconnect()
```

---

## MT5 Windows Bridge

```python
# mt5-bridge/main.py — runs on Windows VM/machine with MT5 installed
# Exposes REST API that Linux Docker container calls

from fastapi import FastAPI
import MetaTrader5 as mt5

app = FastAPI()

@app.post("/connect")
async def connect(login: int, password: str, server: str):
    if not mt5.initialize():
        return {"success": False, "error": mt5.last_error()}
    if not mt5.login(login, password=password, server=server):
        return {"success": False, "error": mt5.last_error()}
    return {"success": True, "account": mt5.account_info()._asdict()}
```

---

## Anti-Patterns

```
✗ MT5 calls in request path (blocking, slow) — use background worker
✗ Storing raw MT5 credentials without Fernet encryption
✗ Missing reconnect logic when MT5 connection drops
✗ Syncing all history on every tick (use incremental sync with from_dt)
✗ Missing error logging on sync failures
✗ Direct MT5 calls from Linux (MT5 only runs on Windows — use bridge)
```
