# Software Factory — Browser Engineering & Visual QA Plane

## 1. Overview
The **Browser Engineering Plane** equips AI coding agents with sight, user interaction simulation, console error triage, network inspection, accessibility validation, and responsive layout verification directly inside the development feedback loop.

Agents never hallucinate whether a button works, whether an API call succeeded from the UI, or whether layout shifted on mobile devices: the browser executes, inspects, and captures deterministic evidence.

```text
  ┌────────────────────────────────────────────────────────┐
  │                 AGENT INTERACTION LOOP                 │
  └──────────────────────────┬─────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 1. Launch & Navigate Headless / Headful Browser        │
  │    (Playwright CLI / Chrome DevTools MCP / Browser Use)│
  └──────────────────────────┬─────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. Visual & Semantic Inspection                         │
  │    • Compact DOM Snapshot (Accessibility Tree)         │
  │    • Console Message Classification (React, CORS, etc.)│
  │    • Network Waterfall & Status Code Verification      │
  └──────────────────────────┬─────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. Automated Audits                                    │
  │    • axe-core WCAG 2.2 Level AA Compliance             │
  │    • 5-Tier Responsive Viewport Matrix                 │
  │    • Multi-Step User Flow Execution                    │
  └──────────────────────────┬─────────────────────────────┘
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 4. Evidence Persistence                                │
  │    Saved to evidence/browser/ (JSON, PNG, traces)      │
  └────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Backend Architecture
Defined in `registries/browser_registry.yaml` and orchestrated by `core/browser_orchestrator.py`:

| Backend ID | Type | Strengths & Use Cases | Supported Agents |
| :--- | :--- | :--- | :--- |
| `playwright-cli` | CLI | Low token overhead, headless execution, CI-native, fast DOM snapshots | Antigravity, Claude Code, Cursor |
| `chrome-devtools-mcp` | MCP | Deep live inspection, source-mapped stacktraces, payload diffs | Antigravity, Claude Code |
| `playwright-mcp` | MCP | Direct agent tool calling, interactive browser sessions | Antigravity, Cline, Roo Code |
| `browser-use` | Agent Lib | Autonomous exploratory QA of unmapped user journeys | Antigravity, Python |
| `antigravity-browser` | Native | Zero-dependency built-in browser interface | Antigravity |

---

## 3. Console & Network Triage
The browser orchestrator classifies console errors into actionable categories:
- **React Runtime Errors**: `Uncaught TypeError`, undefined property access, unhandled promise rejections.
- **Hydration Mismatches**: Server-rendered HTML differing from client React tree.
- **CORS Violations**: Missing or misconfigured `Access-Control-Allow-Origin` headers.
- **Auth Errors**: 401 Unauthorized / 403 Forbidden token expirations.
- **WebSocket Failures**: Dropped connections or negotiation aborts.

Network traffic is inspected for:
- Non-2xx/3xx HTTP statuses (client 4xx vs server 5xx).
- Latency spikes (>1000ms duration flagged as slow).

---

## 4. Responsive Viewports Matrix
All web applications must pass verification across 5 standard viewport tiers:
1. **Mobile**: 375 × 667 (iPhone SE)
2. **Tablet**: 768 × 1024 (iPad Mini)
3. **Laptop**: 1280 × 800 (MacBook Air)
4. **Desktop**: 1920 × 1080 (FHD standard)
5. **Large Desktop**: 2560 × 1440 (QHD ultra-wide)

---

## 5. CLI Commands & Runbook

```bash
# Check registered browser backend health
python3 factory.py browser status

# Run axe-core accessibility audit
python3 factory.py browser a11y --url http://localhost:3000

# Evaluate 5-tier responsive viewport matrix
python3 factory.py browser responsive --url http://localhost:3000

# Run exploratory agentic QA
python3 factory.py browser explore --url http://localhost:3000 --goal "Test order creation"
```
