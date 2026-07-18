from dataclasses import dataclass
from .enums import OptionType


@dataclass(frozen=True)
class EuropeanOption:
    option_type: OptionType
    strike: float
    maturity: float

    def __post_init__(self):
        if self.strike <= 0:
            raise ValueError("Strike price must be positive.")
        if self.maturity <= 0:
            raise ValueError("Maturity must be positive.")