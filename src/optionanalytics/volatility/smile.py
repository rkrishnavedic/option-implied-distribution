import datetime

from ..models.market import MarketData
from ..models.option import EuropeanOption, OptionChain
from ..models.volatility import VolatilityPoint, VolatilitySmile
from ..pricing.implied_volatility import implied_volatility

def build_smile(
        option_chain: OptionChain, 
        market_data: MarketData, 
        valuation_date: datetime.date
    ) -> VolatilitySmile:
    """
    Builds a volatility smile from an option chain and market data.

    Args:
        option_chain (OptionChain): The option chain containing quotes.
        market_data (MarketData): The market data including spot price, risk-free rate, and volatility.

    Returns:
        VolatilitySmile: A volatility smile object containing the implied volatilities.
    """
    points = []

    expiry = datetime.date.fromisoformat(option_chain.expiry)
    maturity = (expiry - valuation_date).days / 365.0  # Convert days to years

    for quote in option_chain.quotes:
        option = EuropeanOption(
            option_type=quote.option_type,
            strike=quote.strike,
            maturity=maturity
        )
        implied_vol = implied_volatility(
            price=quote.mid_price,
            option=option,
            market_data=market_data
        )
        points.append(VolatilityPoint(strike=quote.strike, implied_volatility=implied_vol))

    return VolatilitySmile(underlying=option_chain.underlying, expiry=option_chain.expiry, points=points)