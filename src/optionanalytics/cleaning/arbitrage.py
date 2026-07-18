import math
from datetime import date

from ..models.market import MarketData
from ..models.option import OptionChain
from ..models.enums import OptionType
from ..utils.dates import year_fraction


def filter_price_bound_violations(
    option_chain: OptionChain,
    market_data: MarketData,
    valuation_date: date,
) -> OptionChain:
    """
    Removes option quotes that violate the no-arbitrage price bounds.

    An implied volatility exists only if the observed market price lies within
    the theoretical no-arbitrage bounds implied by the Black-Scholes model.
    Quotes outside these bounds cannot be explained by any positive volatility,
    causing the implied volatility solver to fail.

    Such violations commonly arise in real market data due to stale quotes,
    wide bid-ask spreads, asynchronous updates between the underlying and the
    option market, or other market microstructure effects. Filtering these
    quotes improves the robustness of downstream smile and surface construction.

    Parameters
    ----------
    option_chain : OptionChain
        Option chain to validate against the no-arbitrage price bounds.
    market_data : MarketData
        Current market data containing the spot price and risk-free rate.
    valuation_date : date
        Date on which the option chain is being valued. Used to compute
        the time to expiry.

    Returns
    -------
    OptionChain
        A new option chain containing only quotes that satisfy the
        no-arbitrage price bounds.
    """

    maturity = year_fraction(option_chain.expiry, valuation_date)
    discount_factor = math.exp(-market_data.risk_free_rate * maturity)
    filtered_quotes = []

    for quote in option_chain.quotes:
        market_price = quote.mid_price

        if quote.option_type == OptionType.CALL:
            lower_bound = max(
                market_data.spot - quote.strike * discount_factor,
                0.0,
            )
            upper_bound = market_data.spot
        else:
            lower_bound = max(
                quote.strike * discount_factor - market_data.spot,
                0.0,
            )
            upper_bound = quote.strike * discount_factor

        if lower_bound <= market_price <= upper_bound:
            filtered_quotes.append(quote)

    return OptionChain(
        underlying=option_chain.underlying,
        expiry=option_chain.expiry,
        quotes=filtered_quotes
    )