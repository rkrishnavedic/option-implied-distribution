from dataclasses import dataclass


@dataclass(frozen=True)
class MarketData:
    spot: float
    risk_free_rate: float
    volatility: float

    def __post_init__(self):
        if self.spot <= 0:
            raise ValueError("Spot price must be positive.")
        if self.risk_free_rate < 0:
            raise ValueError("Risk-free rate cannot be negative.")
        if self.volatility <= 0:
            raise ValueError("Volatility must be positive.")