from dataclasses import dataclass
from .enums import OptionType


@dataclass(frozen=True)
class VolatilityPoint:
    strike: float
    implied_volatility: float
    option_type: OptionType


@dataclass(frozen=True)
class VolatilitySmile:
    underlying: str
    expiry: str
    points: list[VolatilityPoint]

@dataclass(frozen=True)
class VolatilitySurface:
    underlying: str
    smiles: list[VolatilitySmile]