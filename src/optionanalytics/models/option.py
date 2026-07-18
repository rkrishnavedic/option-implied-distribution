from dataclasses import dataclass
from datetime import datetime, date
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
        
@dataclass(frozen=True)
class OptionQuote:
    """Represents a single option quote with its associated data."""
    option_type: OptionType

    strike: float

    bid: float
    ask: float
    last_price: float

    @property
    def mid_price(self) -> float:
        return (self.bid + self.ask) / 2

    volume: int | None
    open_interest: int

    last_trade_time: datetime

    def __post_init__(self):
        if self.strike <= 0:
            raise ValueError("Strike price must be positive.")
        if self.bid < 0:
            raise ValueError("Bid price cannot be negative.")
        if self.ask < 0:
            raise ValueError("Ask price cannot be negative.")
        if self.last_price < 0:
            raise ValueError("Last price cannot be negative.")
        if self.volume is not None and self.volume < 0:
            raise ValueError("Volume cannot be negative.")
        if self.open_interest < 0:
            raise ValueError("Open interest cannot be negative.")
        if not isinstance(self.last_trade_time, datetime):
            raise ValueError("Last trade time must be a datetime object.")

@dataclass(frozen=True)
class OptionChain:
    """All listed options for one underlying asset with the same expiration date."""
    underlying: str
    expiry: date
    quotes: list[OptionQuote]