# MT5 Gateway & Worker: Scaling, Queue & Capacity Specification
**Integral Market Software Factory — High-Throughput Broker Integration Engine**  
**Document ID:** `IM-SPEC-MT5-WORKER-001`  
**Status:** Approved for Production Deployment  
**Runtime:** Podman / Docker (Linux + Wine64 + Python 3.12 + MetaTrader 5 API)

---

## 1. Executive Summary

MetaTrader 5 (MT5) requires a Windows execution runtime because MetaQuotes distributes the core IPC terminal and client DLLs exclusively for Win32/Win64. 

This specification defines the production **Docker/Podman containerized MT5 worker architecture**, combining:
1. **Headless Linux Runtime**: Debian Bookworm with 64-bit Wine and virtual Xvfb display.
2. **Native Python 3.12 64-bit Engine**: Windows Python 3.12 running under Wine hosting the official `MetaTrader5` package (v5.0.6231).
3. **Dual-Role Gateway Worker**:
   - **HTTP REST Gateway** (FastAPI on `:9100`) for low-latency interactive requests (account info, tick data, order execution).
   - **Distributed Queue Worker** for scheduled, high-throughput asynchronous account sync via Redis.
4. **Resilient Scaling Topology**:
   - Zero Single Point of Failure (NSPF).
   - Horizontal worker autoscaling across N instances.
   - Dual-priority queue with atomic claiming and dead-letter queues.

---

## 2. Container Architecture & Supervision Tree

Inside each container instance, an integrated supervisor (`entrypoint.sh`) maintains the process lifecycle with self-healing watchdogs:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   integral-mt5-worker Container                        │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ entrypoint.sh (Supervisor, Watchdog & Signal Trap)              │   │
│   └──────┬───────────────┬─────────────────┬───────────────────┬───┘   │
│          │               │                 │                   │       │
│          ▼               ▼                 ▼                   ▼       │
│     ┌─────────┐   ┌─────────────┐   ┌─────────────┐   ┌────────────┐   │
│     │ Xvfb    │   │ MT5 Terminal│   │ MT5 Bridge  │   │ Queue      │   │
│     │ (:99)   │   │(terminal64) │   │ FastAPI     │   │ Worker     │   │
│     │         │   │ (Headway)   │   │ (:9100)     │   │ (Redis)    │   │
│     └─────────┘   └─────────────┘   └─────────────┘   └────────────┘   │
│                          ▲                 ▲                 ▲         │
│                          │                 │                 │         │
│                          └────── IPC ──────┴─────────────────┘         │
│                                (Shared memory / Named pipes)           │
└────────────────────────────────────────────────────────────────────────┘
```

### Self-Healing Watchdog
The container supervisor runs a 10-second heartbeat check:
- If `Xvfb` crashes, it restarts the virtual display buffer.
- If `bridge.py` crashes, it restarts the HTTP server without killing the MT5 terminal.
- If `queue_worker.py` crashes, it re-registers in Redis and resumes queue processing.
- If the container is stopped (`SIGTERM`), it safely shuts down IPC pipes, flushes pending jobs back to Redis, and exits cleanly.

---

## 3. Redis Queue Architecture & Error Taxonomy

```
                   User Requests (Interactive UI)
                                │
                                ▼
                   ┌───────────────────────────┐
                   │ mt5:sync:priority_queue   │  (High Priority)
                   └─────────────┬─────────────┘
                                 │
Scheduled Background Sync        │
           │                     │
           ▼                     │
┌───────────────────────────┐    │
│ mt5:sync:queue            │    │  (Standard Priority)
└──────────┬────────────────┘    │
           │                     │
           └──────────┬──────────┘
                      │
                      ▼ RPOPLPUSH (Atomic Claim)
┌───────────────────────────────────────────────┐
│ mt5:sync:processing:{worker_id}               │
└─────────────────────┬─────────────────────────┘
                      │
           ┌──────────┴──────────┐
           ▼                     ▼
     [Success]              [Failure]
           │                     │
  ┌────────┴────────┐   ┌────────┴────────┐
  │ - Cache (TTL30s)│   │ Retry < Max?    │
  │ - DB Upsert     │   ├───────┬─────────┤
  │ - WS Broadcast  │   │ YES   │ NO      │
  │ - LREM process  │   ▼       ▼         │
  └─────────────────┘ Backoff  Dead Letter│
                      Re-queue Queue (DLQ)│
```

### Timestamped Job Payload Schema
Every task enqueued into Redis carries microsecond precision timing telemetry:
```json
{
  "job_id": "mt5_sync_4f7e21a8-8b01-49b2-b13c-e09a87d19012",
  "account_id": "b18f0c29-37e4-4d89-9831-29d10e527038",
  "login": 5052828,
  "server": "Headway-Live",
  "password": "...",
  "operation": "SYNC_ACCOUNT",
  "enqueued_at": "2026-10-02T11:20:00.123456Z",
  "enqueued_ts": 1727858400.123,
  "priority": 10,
  "retry_count": 0,
  "max_retries": 3,
  "timeout_seconds": 25.0
}
```

### Error Taxonomy
| Error Code | Classification | Action |
| :--- | :--- | :--- |
| `MT5_AUTH_FAILED` | Permanent | **No retry.** Update account status to `auth_error` in DB, alert user. |
| `MT5_SERVER_UNREACHABLE` | Transient | **Retry with exponential backoff** (3x: 3s, 6s, 12s). |
| `MT5_TERMINAL_NOT_READY` | Transient | **Immediate re-queue** with 2s delay. |
| `MT5_TRADE_TIMEOUT` | Critical | **Verify order status** before retrying to prevent duplicate orders. |
| `MT5_RATE_LIMITED` | Transient | **Pause worker account pool** for 60 seconds. |
| `MT5_CIRCUIT_OPEN` | System | **Circuit breaker opened** after 5 consecutive failures. Pauses for 60s. |

---

## 4. Concrete Capacity Analysis: 1 Single Worker

### A. Execution Latency Profile (Per Account Sync)
| Step | Operation | Duration |
| :--- | :--- | :--- |
| 1 | Dequeue job from Redis & verify connection | **5ms - 15ms** |
| 2 | MT5 terminal login verify (`account_info()`) | **30ms - 80ms** |
| 3 | Query open positions (`positions_get()`) | **25ms - 60ms** |
| 4 | Query incremental deals (last 7 days history) | **60ms - 180ms** |
| 5 | Cache positions in Redis (`SETEX TTL 30s`) | **2ms - 5ms** |
| 6 | Publish WebSocket update event to subscribers | **1ms - 3ms** |
| 7 | Batch upsert into PostgreSQL `journal.trade_analytics` | **25ms - 60ms** |
| **Total** | **Average Execution Cycle Duration** | **~350ms – 500ms** |

---

### B. Mathematical Throughput for 1 Single Worker

$$\text{Throughput (Syncs/Sec)} = \frac{1}{\text{Latency (sec)}} = \frac{1}{0.400\text{s}} = \mathbf{2.5 \text{ syncs / second}}$$

#### 1. Per-Minute Capability (1 Worker):
- **Conservative Baseline** (500ms per sync):  
  $$2.0 \times 60 = \mathbf{120 \text{ user accounts synced per minute}}$$
- **Optimized Peak** (350ms per sync):  
  $$2.85 \times 60 = \mathbf{171 \text{ user accounts synced per minute}}$$

#### 2. Per-Hour Capability (1 Worker):
- **Conservative Baseline**:  
  $$120 \times 60 = \mathbf{7,200 \text{ user account syncs per hour}}$$
- **Optimized Peak**:  
  $$171 \times 60 = \mathbf{10,260 \text{ user account syncs per hour}}$$

---

### C. Real-World User Capacity Modes for 1 Single Worker

| Sync Operating Model | Sync Interval | Continuous Users Served by 1 Worker | User Experience |
| :--- | :--- | :--- | :--- |
| **Aggressive Real-Time** | Every **1 minute** | **120 – 170 users** | Ultra-responsive scalper experience (1 min updates) |
| **Standard Active Trading** | Every **5 minutes** | **600 – 850 users** | Standard professional trading journal sync interval |
| **Smart Adaptive Mode** *(Recommended)* | **1 min** (Active on UI)<br>**15 min** (Background) | **1,800 – 2,500 users** | Optimal resource usage: 10% active viewers + 90% background sync |
| **Interactive Read Queries** | Sub-10ms (Redis Cache) | **50,000+ reads/sec** | Instantaneous dashboard loads powered by Redis TTL cache |

---

## 5. Horizontal Scaling & Zero Single Point of Failure (NSPF)

To scale beyond a single worker, simply scale the container pool using Podman or Docker Compose:

```bash
# Scale to 3 active worker nodes
podman compose -f podman-compose.yml up --scale mt5-worker=3 -d
```

### Scaling Matrix
| Worker Count | Syncs / Second | Syncs / Minute | Syncs / Hour | Active Users (5-min Sync) | Adaptive Users (Tiered) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Worker** | 2.5/s | 150/min | 9,000/hr | **750 users** | **2,200 users** |
| **2 Workers** | 5.0/s | 300/min | 18,000/hr | **1,500 users** | **4,500 users** |
| **4 Workers** | 10.0/s | 600/min | 36,000/hr | **3,000 users** | **9,000 users** |
| **10 Workers** | 25.0/s | 1,500/min | 90,000/hr | **7,500 users** | **22,500 users** |

### High Availability Guarantees
1. **Dynamic Work Distribution**: Redis `RPOPLPUSH` ensures jobs are distributed fairly without central master bottlenecks.
2. **Automatic Crash Recovery**: If Worker 1 terminates while processing an account, its atomic processing list (`mt5:sync:processing:worker-1`) is re-queued into the priority queue by healthy workers or upon watchdog restart.
3. **No Duplicate Execution**: Redis distributed locking (`SET lock:acct:{id} worker_id NX EX 30`) prevents two workers from processing the same trading account simultaneously.
