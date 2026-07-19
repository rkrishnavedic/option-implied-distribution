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

    def __post_init__(self):
        if not self.smiles:
            raise ValueError("Volatility surface cannot be empty.")

        if any(smile.underlying != self.underlying for smile in self.smiles):
            raise ValueError("All smiles must belong to the same underlying.")