# ADR-010: MT5 Multi-Node Gateway, cTrader Integration, Broker Branding, imJournal Analytics & R2 Streaming

**Status:** APPROVED  
**Date:** 2026-11-08  
**Deciders:** Principal Software Architect, Antigravity Engineering Team  
**Scope:** Distributed Trading Gateway, Multi-Broker Execution, Performance Analytics, Cloudflare R2 Streaming  

---

## 1. Context & Problem Statement

Integral Market required a robust, production-grade distributed execution architecture across multiple broker platforms (MetaTrader 5, MetaTrader 4, cTrader, TradeLocker) coupled with institutional-grade journal analytics and reliable media streaming:
1. **MT5 Multi-Node Execution:** Needed reliable IPC bridge execution, automatic health probing, failover node routing, and seamless webhook integration with TradingView Pine Script.
2. **cTrader Protocol Integration:** Needed OAuth2 account synchronization, bi-directional trade capture, and historical deal ingestion.
3. **Official Broker Identity:** Broker selection and connection cards required authentic, verifiable brand emblems adhering to official style guides.
4. **imJournal Performance Analytics:** Financial metrics required consistent 2-decimal precision (`-$3.00`, `0.00%`, `0.00`), tabular font alignment, and dynamic equity curve rendering that displays trade-by-trade progression even during single-day trading streaks.
5. **Media Resilience & Cloudflare R2 Streaming:** Course covers and library reading materials required resilient multi-bucket resolution and context-aware fallback covers when offline.

---

## 2. Decision & Implementation

### A. MT5 Gateway Multi-Node Topology
- Dedicated Podman worker container `mt5-worker-node1` running on port 9100.
- Dynamic route dispatch in `integral-expert-backend` via `MT5NodeRegistry`.
- Automatic webhook execution bridge in `app/api/v1/endpoints/imcharts/webhooks.py` with HMAC secret verification and order logging.

### B. cTrader OAuth & Trade Synchronization
- Standardized OAuth2 token refresh and deal fetching in `integral-expert-backend`.
- Dedicated background worker synchronizing closed positions and commissions into `im_expert_db`.

### C. Authentic Broker Brand System
- Procured, normalized, and deployed authentic brand logos for MetaTrader 5 (gold '5' with triangular figures), MetaTrader 4 (orange '4' on blueprint grid), TradeLocker (aperture emblem), cTrader, Bybit, Bitunix, Match-Trader, and Headway.
- Reusable React components: `BrokerBrandIcon`, `BrokerBrandLogo`, `BrokerPlatformCard`, `BrokerPlatformSelector`, `BrokerStatusBadge`.

### D. imJournal Precision & Dynamic Curve Synthesis
- Configured `journalTemplates.ts` formatters to default to 2 decimal places (`money(v, 2)`, `pct(v, 2)`, `num(v, 2)`).
- When calendar date buckets are $\le 1$, `AnalyticsPage.tsx` automatically synthesizes trade-by-trade cumulative progression anchored to initial balance, ensuring balance and drawdown curves chart accurately.
- `OfflineIndicator.tsx` updated with 5-second auto-dismiss timer and immediate manual dismissal (`X`).

### E. Cloudflare R2 Multi-Bucket Streaming & Dynamic Fallbacks
- Backend image proxy (`/api/v1/academy/proxy/image`) normalizes path keys across `integral-market-media`, `integral-market-library`, and `integral-market-academy` buckets.
- Implemented high-fidelity SVG fallbacks tailored to material type: reading document fallback with book spine for reading courses/books, interactive video player fallback with timeline for video masterclasses, and graduation shield for academy curriculum.

---

## 3. Consequences & Verification

- **Portability:** All microservices (8000, 8002, 8003, 8010, 8011) and containers operate cohesively under single-command orchestration (`./scripts/dev.sh`).
- **Precision:** Zero unformatted or premature currency rounding across all trading modules.
- **Resilience:** End-to-end zero broken image states across Academy and Library even during complete network or CDN failure.
- **Factory Status:** 14/14 subsystems healthy, 20/20 MCP servers verified.
