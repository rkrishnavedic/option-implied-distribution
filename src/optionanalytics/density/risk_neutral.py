"""
Risk-neutral density extraction using the Breeden-Litzenberger formula.

The density is recovered by numerically differentiating a smooth European
call price function with respect to strike:

    f(K) = exp(rT) * d²C/dK²

where the call price function is constructed by combining Black-Scholes
pricing with an interpolated implied volatility smile.
"""

from datetime import date
import numpy as np
from collections.abc import Callable

from ..volatility.svi import build_svi
from ..volatility.interpolation import interpolate_smile
from ..utils.dates import year_fraction
from ..pricing.black_scholes import black_scholes

from ..models.density import Density, DensityPoint
from ..models.volatility import VolatilitySmile
from ..models.market import MarketData
from ..models.enums import InterpolationMethod, OptionType, VolatilityModel
from ..pricing.black_scholes import EuropeanOption

NUMBER_OF_DATA_POINTS=300

def _price_from_smile(
        strike: float, 
        iv_function: Callable[[float], float], 
        maturity: float, 
        market_data: MarketData
    ) -> float:
    call_price = EuropeanOption(OptionType.CALL, strike=strike, maturity=maturity)

    sigma = iv_function(strike)
    iv_market_data = MarketData(
        spot=market_data.spot, 
        risk_free_rate=market_data.risk_free_rate, 
        volatility=sigma
    )
    
    return black_scholes(option=call_price, market=iv_market_data)

def _second_derivative(
        prices: np.ndarray,
        strikes: np.ndarray,
    ) -> np.ndarray:
    """
    Computes the second derivative of option prices with respect to strike.
    """
    first = np.gradient(prices, strikes)
    second = np.gradient(first, strikes)
    return second

def build_density(
        smile: VolatilitySmile,
        market_data: MarketData,
        valuation_date: date,
        interpolation_method: InterpolationMethod = InterpolationMethod.PCHIP,
        volatility_model: VolatilityModel | None = None,
        number_of_data_points: int = NUMBER_OF_DATA_POINTS
    ) -> Density:

    maturity = year_fraction(
        expiry=smile.expiry,
        valuation_date=valuation_date,
    )

    if volatility_model is None:
        iv_function = interpolate_smile(
            smile,
            interpolation_method,
        )
    elif volatility_model == VolatilityModel.SVI:
        iv_function = build_svi(
            smile,
            market_data,
            maturity
        )
    else:
        raise ValueError(f"Unsupported volatility model: {volatility_model}")

    strikes = [p.strike for p in smile.points]

    K = np.linspace(
        min(strikes),
        max(strikes),
        number_of_data_points,
    )

    C = np.array([
        _price_from_smile(k, iv_function, maturity, market_data)
        for k in K
    ])

    d2C_dK2 = _second_derivative(C, K)

    discount_factor = np.exp(
        market_data.risk_free_rate * maturity
    )

    density_points = [
        DensityPoint(
            strike=float(k),
            probability_density=float(max(discount_factor * pdf, 0.0)),
        )
        for k, pdf in zip(K, d2C_dK2)
    ]

    return Density(
        underlying=smile.underlying,
        expiry=smile.expiry,
        points=density_points,
    )