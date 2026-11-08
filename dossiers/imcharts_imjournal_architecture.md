# IMCharts + IM Journal — System Architecture Dossier

**Document Version:** 1.0.0  
**Status:** Approved for Implementation  
**Target Services:** `integral-expert-backend` (Port 8002), `infrastructure/mt5-worker` (Port 9100), `app` (Frontend Preview Port 5173), `im_expert_db` (PostgreSQL 5432)

---

## 1. Executive Summary & Core Engineering Axiom

The **Integral Market** platform requires an institutional-grade, unified manual chart trading and trade journaling environment. Previously, account models across onboarding, execution, and journaling contained divergence risks between `broker_connections.accounts` and `journal.trading_accounts`.

**The Supreme Canonical Account Rule:**
There is exactly **one canonical broker account** per user brokerage connection. Every execution request in IMCharts, every synced trade in IM Journal, every risk rule check, and every chart workspace MUST resolve to the canonical identifier:
$$\text{Account ID} \equiv \text{broker\_connections.accounts.id} \equiv \text{journal.trading\_accounts.broker\_account\_id}$$

Under no circumstances may an account exist in IMCharts without immediate visibility in IM Journal, nor may an account connected in IM Journal fail to execute in IMCharts.

---

## 2. Service Boundaries & System Topology

```mermaid
flowchart TB
    subgraph Frontend ["Frontend Single-Page App (React + Vite :5173)"]
        IMCharts["IMCharts Trading Canvas\n(/expert/charts)"]
        IMJournal["IM Journal Dashboard & Trades\n(/expert/journal)"]
        Store["Canonical useBrokerAccountStore\n(localStorage: 'im-active-broker')"]
        IMCharts <--> Store
        IMJournal <--> Store
    end

    subgraph GatewayProxy ["Vite Reverse Proxy (:5173)"]
        ViteRoute["/api/v1/brokers/*\n/api/v1/imcharts/*\n/api/v1/journal/*"]
    end

    subgraph ExpertBackend ["Integral Expert Backend (FastAPI :8002)"]
        BrokerAPI["/api/v1/brokers\n• Accounts CRUD\n• Unified Broker Search\n• Server Submission"]
        ChartsAPI["/api/v1/imcharts\n• UDF History / Quotes\n• Direct Order Execution\n• Positions & Ticks"]
        JournalAPI["/api/v1/journal\n• Deals & Trades Reconcile\n• Performance Analytics\n• Trade Review & Tags"]
        ExecEngine["Execution Engine\n(Priority Execution Lane)"]
        SyncEngine["Universal Sync Engine\n(Background Sync Lane)"]
        BrokerRegistry["BrokerRegistry & Adapters\n(MT5, cTrader, MT4)"]
    end

    subgraph MT5Infra ["Hosted MT5 Infrastructure (:9100)"]
        MT5Worker["MT5 Worker Bridge (Wine + Python 3.12)\n• terminal64.exe\n• MetaTrader5 5.0.6231\n• multi-account switcher"]
        RedisQueues["Redis (Port 6379)\n• mt5:sync:priority_queue (Execution)\n• mt5:sync:queue (Sync Backfill)"]
    end

    subgraph Database ["PostgreSQL (:5432 - im_expert_db)"]
        BCA["broker_connections.accounts\n(Master Connection State)"]
        JTA["journal.trading_accounts\n(pointer: broker_account_id)"]
        JTJ["journal.trading_journals"]
        JTR["journal.trade_analytics\n(Canonical Trades & Deals)"]
        MB["journal.mt5_brokers (103)"]
        MS["journal.mt5_servers (214)"]
    end

    Frontend --> GatewayProxy
    GatewayProxy --> ExpertBackend
    ExpertBackend --> Database
    ExpertBackend --> MT5Infra
    MT5Worker --> RedisQueues
```

---

## 3. Canonical Account Data Model & State Machine

### 3.1 Relational Schema Alignment
1. **Master Connection Record**: `broker_connections.accounts`
   - `id` (UUID): The authoritative system-wide account identifier.
   - `user_id` (UUID): Account owner.
   - `broker_name`: e.g. "Exness", "Headway", "IC Markets".
   - `server`: Exact broker server name matching MT5 terminal (e.g. `Exness-MT5Real`, `Headway-Demo`).
   - `account_number`: Login ticket.
   - `credentials_encrypted`: Fernet/AES-GCM encrypted payload (`{"password": "...", "server": "..."}`).
   - `connection_status`: `'connected'`, `'stale'`, `'disconnected'`, `'error'`.
   - `is_demo`: Boolean.
   - `last_balance`, `last_equity`, `last_margin`, `last_free_margin`, `currency`, `leverage`.

2. **Journal Account Pointer**: `journal.trading_accounts`
   - `id` (UUID): Internal journal account ID.
   - `broker_account_id` (UUID): Foreign key strictly referencing `broker_connections.accounts.id`.
   - `user_id` (UUID): Matches owner.
   - `lifecycle_state`: `'active'`, `'provisioning'`, `'connected'`, `'stale'`, `'suspended'`.

3. **Trading Journal Record**: `journal.trading_journals`
   - `account_id` (UUID): points to `journal.trading_accounts.id`.
   - `unified_account_id` (UUID): points to `broker_connections.accounts.id`.

### 3.2 Account Connection Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> Submitting: User Enters Credentials
    Submitting --> Validating: Format & Server Verification
    Validating --> GatewayAuth: Test Connection via MT5 Worker (:9100)
    GatewayAuth --> Provisioning: Authentication Succeeded
    GatewayAuth --> ErrorState: Authentication Failed (Invalid Server/Login)
    
    Provisioning --> Connected: Persist Master BCA + Pointer JTA
    Connected --> Executing: IMCharts Manual Trade Placement
    Connected --> Syncing: Incremental Deal Synchronization
    
    Executing --> Connected: Position Opened/Closed
    Syncing --> Connected: Deals Persisted to journal.trade_analytics
    
    Connected --> Stale: Gateway Heartbeat Timeout / Password Changed
    Stale --> GatewayAuth: Re-enter Credentials / Auto-Reconnect
    Connected --> [*]: User Deregisters Account
```

---

## 4. MT5 Gateway Dual-Lane Execution & Sync Architecture

To prevent long-running history synchronization or bulk backfills from blocking high-priority manual order execution in IMCharts, the system implements **Lane Separation**:

1. **High-Priority Execution Lane (`mt5:sync:priority_queue`)**:
   - Market orders, limit orders, SL/TP modifications, and position closures.
   - Execution timeout: $\le 3000\text{ ms}$.
   - Directly interrupts non-critical polling.
   - Emits `trade.opened`, `trade.closed`, `trade.modified` to Redis Streams immediately.

2. **Standard Background Sync Lane (`mt5:sync:queue`)**:
   - Initial 90-day history backfill, periodic candle updates, and daily deal reconciliation.
   - Concurrency controlled to prevent terminal IPC lock contention.
   - Reconciles individual MT5 deals (`ENTRY_IN`, `ENTRY_OUT`, `ENTRY_INOUT`) into atomic closed trades in `journal.trade_analytics`.

---

## 5. Frontend Unified Store Architecture

The frontend leverages `useBrokerAccountStore` (`im-active-broker` in localStorage):
- **Selected Account ID**: References canonical `broker_connections.accounts.id`.
- Selecting an account in the IMCharts header (`BrokerSelector`) automatically updates:
  1. `ChartCanvas`: refreshes tick subscriptions, symbol permissions, and trade markers.
  2. `OrderPanel`: binds account balance, risk calculations, and execution tickets.
  3. `BottomPanel`: streams active positions and open orders for the selected account.
  4. `TradingJournalModule` & `TradeHistoryPage`: filters trades and analytics to the active account seamlessly.
