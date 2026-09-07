# Integral Market — Financial Execution Policy

## Core Principle
Under no circumstances may any autonomous agent, MCP server, or background script execute live capital orders without explicit, multi-factor authorization.

## Prohibited Autonomous Operations
1. Live MT4/MT5 trade execution (`OrderSend`, `OrderClose`, `OrderModify`).
2. Binance / crypto exchange mainnet API order placement or withdrawals.
3. Live broker account balance manipulation or funds transfers.

## Permitted Operations
1. Simulation & paper trading (Alpaca paper environment, MT5 demo testbed).
2. Historical backtesting & tick strategy replay.
3. Quantitative market data extraction & indicator computation.
