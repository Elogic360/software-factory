"""
Event-Driven Strategy Backtest Template (Ziplime / Pandas / Polars compatible)
"""
from dataclasses import dataclass
from typing import List, Dict
import pandas as pd
import numpy as np

@dataclass
class BacktestResult:
    total_return: float
    cagr: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int

def run_strategy_backtest(df: pd.DataFrame, initial_capital: float = 100000.0) -> BacktestResult:
    """
    Computes standard performance metrics on an OHLCV dataframe with a 'signal' column (1: buy, -1: sell, 0: hold).
    """
    if "signal" not in df.columns or "close" not in df.columns:
        raise ValueError("DataFrame must contain 'signal' and 'close' columns")

    df = df.copy()
    df["returns"] = df["close"].pct_change()
    df["strategy_returns"] = df["returns"] * df["signal"].shift(1)
    df["cumulative"] = (1 + df["strategy_returns"].fillna(0)).cumprod()
    df["peak"] = df["cumulative"].cummax()
    df["drawdown"] = (df["cumulative"] - df["peak"]) / df["peak"]

    total_ret = float(df["cumulative"].iloc[-1] - 1.0) if len(df) > 0 else 0.0
    mean_ret = df["strategy_returns"].mean()
    std_ret = df["strategy_returns"].std()
    sharpe = float((mean_ret / std_ret) * np.sqrt(252)) if std_ret and std_ret > 0 else 0.0
    max_dd = float(df["drawdown"].min()) if len(df) > 0 else 0.0

    return BacktestResult(
        total_return=round(total_ret, 4),
        cagr=round(total_ret, 4),
        sharpe_ratio=round(sharpe, 2),
        max_drawdown=round(max_dd, 4),
        win_rate=round(float((df["strategy_returns"] > 0).mean()), 4) if len(df) > 0 else 0.0,
        total_trades=int((df["signal"].diff().abs() > 0).sum())
    )
