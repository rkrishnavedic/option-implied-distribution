from typing import Callable

import numpy as np
from scipy.optimize import minimize

from ..models.market import MarketData
from ..models.svi import SVIParameters
from ..models.volatility import VolatilitySmile

def forward_price(
    market_data: MarketData,
    maturity: float,
) -> float:
    return (
        market_data.spot
        * np.exp(market_data.risk_free_rate * maturity)
    )

def log_moneyness(
    strike: float,
    forward: float,
) -> float:
    return np.log(strike / forward)

def total_variance(
    log_moneyness: float,
    parameters: SVIParameters,
) -> float:
    """
    Evaluates the raw SVI total implied variance parameterization.

    Parameters
    ----------
    log_moneyness : float
        Log-forward moneyness, ln(K / F).

    parameters : SVIParameters
        Raw SVI parameters.

    Returns
    -------
    float
        Total implied variance w(k).
    """
    x = log_moneyness - parameters.m

    return (
        parameters.a
        + parameters.b
        * (
            parameters.rho * x
            + np.sqrt(x * x + parameters.sigma**2)
        )
    )


def implied_volatility(
    log_moneyness: float,
    maturity: float,
    parameters: SVIParameters,
) -> float:
    """
    Converts SVI total implied variance into implied volatility.
    """
    return np.sqrt(
        total_variance(log_moneyness, parameters) / maturity
    )

def calibration_data(
    smile: VolatilitySmile,
    market_data: MarketData,
    maturity: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Converts a volatility smile into the (k, w) observations used for
    SVI calibration.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        k : log-moneyness
        w : total implied variance
    """
    forward = forward_price(
        market_data,
        maturity,
    )

    k = np.array([
        log_moneyness(
            point.strike,
            forward,
        )
        for point in smile.points
    ])

    w = np.array([
        point.implied_volatility**2 * maturity
        for point in smile.points
    ])

    return k, w


def objective_function(
    x: np.ndarray,
    k: np.ndarray,
    observed_w: np.ndarray,
) -> float:
    """
    Least-squares objective for SVI calibration.
    """
    svi = SVIParameters(
        a=x[0],
        b=x[1],
        rho=x[2],
        m=x[3],
        sigma=x[4],
    )

    model_w = total_variance(
        k,
        svi,
    )

    return np.mean(
        (model_w - observed_w) ** 2
    )


def calibrate_svi(
    smile: VolatilitySmile,
    market_data: MarketData,
    maturity: float,
) -> SVIParameters:
    """
    Calibrates the raw SVI parameterization to an implied volatility smile.
    """
    k, observed_w = calibration_data(
        smile,
        market_data,
        maturity,
    )

    initial_guess = np.array([
        -0.05,   # a
        0.2,                # b
        -0.3,                # rho
        0.0,                # m
        0.2,                # sigma
    ])

    bounds = [
        (None, None),      # a
        (0.0, None),      # b
        (-0.999, 0.999),  # rho
        (None, None),     # m
        (1e-6, None),     # sigma
    ]

    result = minimize(
        objective_function,
        x0=initial_guess,
        args=(k, observed_w),
        bounds=bounds,
        method="L-BFGS-B",
    )

    if not result.success:
        raise RuntimeError(
            f"SVI calibration failed: {result.message}"
        )

    return SVIParameters(
        a=result.x[0],
        b=result.x[1],
        rho=result.x[2],
        m=result.x[3],
        sigma=result.x[4],
    )

def build_svi(
    smile: VolatilitySmile,
    market_data: MarketData,
    maturity: float,
) -> Callable[[float], float]:
    parameters = calibrate_svi(
        smile,
        market_data,
        maturity,
    )

    forward = forward_price(
        market_data,
        maturity,
    )

    def iv_function(strike: float) -> float:
        k = log_moneyness(
            strike,
            forward,
        )

        return implied_volatility(
            log_moneyness=k,
            maturity=maturity,
            parameters=parameters,
        )

    return iv_function