# TradingView Alert Setup & Pine Script v6 Quick Start Guide

**Project:** Integral Market  
**Feature:** IMCharts Execution Bridge  
**Companion Script:** `docs/imcharts/pine-script/Integral_Market_MT5_Execution_Bridge_v1.0.pine`

---

## 1. Quick Start Workflow

Follow these steps to connect your TradingView chart to your MetaTrader 5 account:

### Step 1: Connect your MT5 Account in Integral Market
1. Open Integral Market and navigate to **Connections** (`/expert/connections`).
2. Add your MT5 broker account (Demo or Live). Ensure the account is connected and active.

### Step 2: Generate your Private TradingView Webhook
1. Go to **IMCharts** (`/imcharts` or `/expert/charts`).
2. Click the **TradingView Webhook Bridge** button in the header or toolbar.
3. Select your connected MT5 account.
4. Set your risk guardrails (e.g. Max 2% risk, Max 1.0 lots, 120s timeout).
5. Click **Generate TradingView Webhook**.
6. **Copy the one-time Webhook URL**. Store it securely.

### Step 3: Add Pine Script v6 Indicator to TradingView
1. Open `https://www.tradingview.com/chart/`.
2. Open the **Pine Editor** at the bottom of the screen.
3. Open the **Pine Script v6 Code** tab in the Integral Market Bridge Modal and click **Copy Pine Script**.
4. Paste the code into the Pine Editor, save it as `Integral Market — MT5 Execution Bridge v1.0`, and click **Add to chart**.

### Step 4: Configure your Chart Alert
1. Press `Alt + A` (or right-click the chart and select **Add Alert**).
2. Set **Condition** to `Integral Market — MT5 Execution Bridge v1.0`.
3. Choose **Any alert() function call** or **Integral Market: Send Order Alert**.
4. Check **Webhook URL** and paste your private webhook endpoint:
   `https://api.integralmarket.tech/api/v1/imcharts/webhooks/tradingview/<YOUR_PRIVATE_TOKEN>`
5. Leave the Message field as default (the script dynamically formats the JSON payload).
6. Click **Create**.

---

## 2. Order Sizing & Risk Modes

| Sizing Mode | Pine Script Input | Backend Calculation |
| :--- | :--- | :--- |
| **Risk %** (`RISK_PERCENT`) | `Risk Percentage (%)` (e.g. `1.0%`) | Backend looks up MT5 contract specs (tick size, tick value, contract size) and account equity. Sizes lots so loss at SL matches exact equity %. Rounds down to broker `volume_step`. |
| **Fixed Volume** (`FIXED_VOLUME`) | `Fixed Volume (Lots)` (e.g. `0.10`) | Dispatches specified fixed lot volume, validated against broker `volume_min`, `volume_max`, and webhook limit. |

---

## 3. Order Types Reference

- **Market Orders (`OPEN_MARKET`)**: Enters immediately at market price with Stop Loss and Take Profit levels.
- **Limit Orders (`OPEN_LIMIT`)**: Places pending limit order at `entry_price`.
- **Stop Orders (`OPEN_STOP`)**: Places pending stop order at `entry_price`.
- **Close Orders (`CLOSE`)**: Closes position (`close_percent` 1-100%).
- **Modify Orders (`MODIFY_SLTP`)**: Updates Stop Loss and Take Profit on open positions.

---

## 4. Diagnostics & Live Execution Monitoring

- You can monitor alert arrivals and status transitions in real time from the **Live Execution Feed** tab inside the Integral Market modal.
- Each event details:
  - Timestamp
  - Event Type & Symbol
  - Side & Volume
  - Execution Status (`QUEUED`, `DISPATCHED`, `SUBMITTED_TO_MT5`, `BROKER_ACKNOWLEDGED`, `FILLED`, `REJECTED`)
  - Broker Ticket #
  - Interactive **Audit Trail** button displaying complete transition history
