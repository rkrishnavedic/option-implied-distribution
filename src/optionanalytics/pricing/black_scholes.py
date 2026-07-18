import numpy as np
from .normal import normal_cdf
from ..models.enums import OptionType
from ..models.option import EuropeanOption
from ..models.market import MarketData

def _compute_d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def _compute_d2(d1: float, sigma: float, T: float) -> float:
    return d1 - sigma * np.sqrt(T)

def black_scholes(option: EuropeanOption, market: MarketData) -> float:
    """
    Calculate the Black-Scholes price of a European option.

    Parameters:
    option (EuropeanOption): The European option to price.
    market (MarketData): The market data including spot price, risk-free rate, and volatility.

    Returns:
    float: The Black-Scholes price of the option.
    """

    S = market.spot
    K = option.strike
    T = option.maturity
    r = market.risk_free_rate
    sigma = market.volatility

    d1 = _compute_d1(S, K, T, r, sigma)
    d2 = _compute_d2(d1, sigma, T)
    discount_factor = np.exp(-r * T)

    match option.option_type:
        case OptionType.CALL:
            price = S * normal_cdf(d1) - K * discount_factor * normal_cdf(d2)
        case OptionType.PUT:
            price = K * discount_factor * normal_cdf(-d2) - S * normal_cdf(-d1)
        case _:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")

    return price