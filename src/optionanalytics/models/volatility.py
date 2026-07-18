from dataclasses import dataclass


@dataclass(frozen=True)
class VolatilityPoint:
    strike: float
    implied_volatility: float


@dataclass(frozen=True)
class VolatilitySmile:
    underlying: str
    expiry: str
    points: list[VolatilityPoint]