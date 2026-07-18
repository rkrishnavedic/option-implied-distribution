from scipy import optimize

from ..models.market import MarketData
from ..models.option import EuropeanOption
from .black_scholes import black_scholes

MIN_VOLATILITY = 1e-6
MAX_VOLATILITY = 5.0

def _objective_function(sigma: float, price: float, option: EuropeanOption, market_data: MarketData) -> float:
    trial_market_data = MarketData(spot=market_data.spot,
                                       risk_free_rate=market_data.risk_free_rate,
                                       volatility=sigma)
    return black_scholes(option, trial_market_data) - price


def implied_volatility(price: float, option: EuropeanOption, market_data: MarketData,
                       tolerance: float = 1e-6, max_iterations: int = 100) -> float:
    """
    Calculate the implied volatility of a European option using the Black-Scholes model.

    Parameters:
    price (float): The market price of the option.
    option (EuropeanOption): The European option for which to calculate implied volatility.
    market_data (MarketData): The market data including spot price and risk-free rate.
        Market Inputs. The volatility field is ignored during the inversion.
        
    tolerance (float): Tolerance for convergence.
    max_iterations (int): Maximum number of iterations.

    Returns:
    float: The implied volatility of the option.
    """

    try:
        implied_vol = optimize.brentq(_objective_function, 
                                      MIN_VOLATILITY, MAX_VOLATILITY, 
                                      args=(price, option, market_data), 
                                      xtol=tolerance, maxiter=max_iterations
                                      )
        return implied_vol
    except ValueError as exc:
        raise ValueError("Failed to compute implied volatility.") from exc