from datetime import date
from dataclasses import dataclass

@dataclass(frozen=True)
class DensityPoint:
    strike: float
    probability_density: float

@dataclass(frozen=True)
class Density:
    underlying: str
    expiry: date
    points: list[DensityPoint]