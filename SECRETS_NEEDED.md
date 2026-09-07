# Secrets & API Keys Needed

| Service | Environment Variable | Purpose | Optional / Required | Risk Tier |
| :--- | :--- | :--- | :--- | :--- |
| **Alpha Vantage** | `ALPHAVANTAGE_API_KEY` | Historical & real-time market data | Required for AV feed | READ |
| **FRED Economic Data** | `FRED_API_KEY` | Macroeconomic indicator retrieval | Optional | READ |
| **Finnhub** | `FINNHUB_API_KEY` | Market news & fundamental data | Optional | READ |
| **Financial Modeling Prep**| `FMP_API_KEY` | Financial ratios & company profiles | Optional | READ |
| **Twelve Data** | `TWELVE_DATA_API_KEY` | Forex & multi-asset price feeds | Optional | READ |
| **Alpaca Trading** | `APCA_API_KEY_ID` / `APCA_API_SECRET_KEY` | Paper trading & simulation | Optional | WRITE_BENIGN |
| **Qdrant Vector DB** | `QDRANT_API_KEY` | Sensei RAG knowledge memory | Optional for cloud | READ / WRITE |
| **Langfuse** | `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY`| LLM telemetry & agent tracing | Optional | READ |
| **Sentry** | `SENTRY_DSN` | Cross-backend error tracking | Optional | READ |
