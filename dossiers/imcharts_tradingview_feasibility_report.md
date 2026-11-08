# IMCharts — TradingView Broker Integration Feasibility Report (Phase 1 Gate)

**Date:** 2026-11-03 · **Status:** GATE NOT PASSED — authorization unconfirmed. No native-integration code was written.

## 1. Product definition (unchanged)
Analyse on tradingview.com → order ticket in TradingView → Integral Market → MT5 gateway → broker → IM Journal.
Lightweight Charts (existing `ChartCanvas.tsx`/`OrderPanel.tsx`) does NOT satisfy this. It is retained only as an internal IM Journal visualization.
`tradingview_integration_dossier.md` (previous turn) recommended Lightweight Charts as the "architecture"; it is **superseded** by this report.

## 2. Evidence reviewed
Primary (fetched directly from `tradingview/rest_integrations_docs`, master): `Integration_overview.rst`, `Endpoints.rst`.
Secondary (web search summaries of vendor/partner pages; NOT verified against TradingView-owned pages): eligibility and commercial terms.
`https://www.tradingview.com/policies/` and the full OpenAPI spec (`/rest-api-spec/`) were not reviewed in this pass.

## 3. What the primary docs establish
1. **The REST contract is public**, but the *experience* is not self-service. The integration has two parts: trading (client browser → broker server, requires CORS) and data (TradingView server → broker, `/streaming`, `/symbol_info`, `/history`) unless the broker only uses TradingView symbols plus `/mapping`.
2. **Sandbox access is gated.** To reach the sandbox (`beta-rest.xstaging.tv`) you must (a) pass TradingView's trading and data **autotests on their Jenkins**, then (b) send TradingView your IP addresses (whitelisted), OAuth2 client details if used, and SVG icons. TradingView then gives "further instructions".
3. **Release is gated by TradingView.** Staging → manual tests → production switch; later changes must be confirmed by TradingView before going to production. Both sides run staging and production environments; separate credentials per environment are required.
4. **Authentication** is the broker's choice: `PasswordBearer` (`/authorize`) or `ServerOAuth2Bearer`.
5. **Required endpoints:** `/config`, `/accounts`, `/instruments`, `/orders`, `/state`, plus `/streaming` when needed. Conditional: `/positions`, `/executions`, `/ordersHistory`, `/previewOrder`, `/quotes`, `/depth`, leverage endpoints, `/mapping`, `/permissions`, `/authorize`.

## 4. Not established by primary docs (must be confirmed with TradingView)
| Question | Current knowledge |
|---|---|
| Is a non-broker (software/journal vendor) eligible to be listed? | Secondary sources say a **regulated brokerage** is required. Integral Market is not a broker; MT5 execution is by the user's own broker. **Likely blocker. Unverified.** |
| Commercial/legal agreement, NDA, fees | Secondary sources: partnership agreement + vetting. Terms unknown. |
| Does TradingView accept an aggregator that routes to many third-party brokers? | Unknown. |
| Who is the regulated counterparty / liable party for orders? | Unknown — material for CFD/FX. |
| Market data for the chart | TradingView supplies its own data unless broker supplies `/streaming`; redistribution of MT5 broker feeds needs review. |

## 5. Feasibility verdict
- **Technical:** The existing stack can plausibly satisfy the contract (MT5 bridge already exposes accounts, positions, orders, history, calc margin/profit, order check/send/modify/cancel, symbol info). Gaps: no `/config`/`/accounts`/`/instruments`/`/state` etc. adapter, no TradingView-style token auth, no `/mapping`, no streaming, no execution state machine/idempotency table, single-terminal account switching (not safe for concurrent multi-account execution).
- **Authorization:** UNCONFIRMED. Without TradingView whitelisting/approval the integration cannot appear in the TradingView trading panel on tradingview.com, regardless of how correct our endpoints are.
- **Therefore:** per the release gate, Phases 3–8 (native broker API, execution, E2E tests, production) are **blocked** pending a written answer from TradingView.

## 6. Not permitted / not done
No DOM scraping, extensions, private-API interception, cookie extraction, browser automation, or alert-webhook bridge presented as native.

## 7. Authorized alternatives (for decision, none implemented)
1. **Apply to TradingView** (broker/partner inquiry) and ask the §4 questions in writing. Pre-work that is safe regardless: build endpoints against the public spec and run the public autotests locally.
2. **Partner with a regulated broker/white-label provider** already integrated with TradingView (e.g. TraderEvolution/DXtrade-class vendors) — changes business model.
3. **Licensed TradingView Trading Platform / Advanced Charts library** embedded in an Integral Market page (not tradingview.com; needs TradingView license; satisfies a TradingView-powered order ticket but not criteria 1–2 as written).
4. Keep internal Lightweight Charts IMCharts (exists) — explicitly not the requested product.
5. Alert-webhook → MT5 execution — requires explicit TradingView authorization for alert-driven orders and does not meet criteria 2–7.

## 8. Safe preparatory work (needs approval to start)
Phase 2 audit and the broker-agnostic foundations that every route needs: execution state machine + idempotency, per-account terminal session manager, symbol mapping service, canonical trade sync. These do not depend on the TradingView decision.

## 9. Next actions
- Owner: send inquiry to TradingView (company type, non-broker model, multi-broker MT5 routing, fees, timeline).
- Decide route (§7) before Phase 3.
