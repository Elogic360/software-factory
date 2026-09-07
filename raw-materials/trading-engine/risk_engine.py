"""
Quantitative Risk Engine — Position Sizing & Pre-Trade Validation
"""
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class TradeOrder:
    symbol: str
    order_type: str
    quantity: float
    entry_price: float
    stop_loss: float
    account_balance: float
    max_risk_pct: float = 0.02

class RiskEngine:
    @staticmethod
    def calculate_position_size(account_balance: float, risk_per_trade_pct: float, entry_price: float, stop_loss_price: float) -> float:
        risk_amount = account_balance * risk_per_trade_pct
        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit <= 0:
            return 0.0
        return round(risk_amount / risk_per_unit, 4)

    @staticmethod
    def validate_order(order: TradeOrder) -> Tuple[bool, Optional[str]]:
        if order.quantity <= 0:
            return False, "Quantity must be positive"
        if order.entry_price <= 0:
            return False, "Entry price must be positive"
        if order.stop_loss <= 0:
            return False, "Stop loss is required for risk compliance"
        max_allowed_risk = order.account_balance * order.max_risk_pct
        actual_risk = abs(order.entry_price - order.stop_loss) * order.quantity
        if actual_risk > max_allowed_risk:
            return False, f"Risk exceeds policy limit: {actual_risk:.2f} > {max_allowed_risk:.2f}"
        return True, None
