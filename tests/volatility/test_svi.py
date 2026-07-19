import numpy as np

from optionanalytics.models.enums import OptionType
from optionanalytics.models.market import MarketData
from optionanalytics.models.svi import SVIParameters
from optionanalytics.models.volatility import VolatilitySmile, VolatilityPoint

from optionanalytics.volatility.svi import (
    forward_price,
    log_moneyness,
    total_variance,
    implied_volatility,
    calibration_data,
    objective_function,
    calibrate_svi,
)


def test_forward_price():
    market = MarketData(
        spot=100.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    maturity = 1.0

    expected = 100.0 * np.exp(0.05)

    assert np.isclose(
        forward_price(market, maturity),
        expected,
    )


def test_log_moneyness_at_forward():
    assert np.isclose(
        log_moneyness(
            strike=100.0,
            forward=100.0,
        ),
        0.0,
    )


def test_total_variance_positive():
    params = SVIParameters(
        a=-0.05,
        b=0.30,
        rho=-0.40,
        m=0.00,
        sigma=0.20,
    )

    k = np.linspace(-0.5, 0.5, 50)

    w = total_variance(
        k,
        params,
    )

    assert np.all(w > 0)


def test_implied_volatility_matches_total_variance():
    params = SVIParameters(
        a=-0.05,
        b=0.30,
        rho=-0.40,
        m=0.00,
        sigma=0.20,
    )

    maturity = 0.50

    iv = implied_volatility(
        log_moneyness=0.0,
        maturity=maturity,
        parameters=params,
    )

    expected = np.sqrt(
        total_variance(0.0, params)
        / maturity
    )

    assert np.isclose(iv, expected)


def test_calibration_data():
    maturity = 0.25

    market = MarketData(
        spot=100.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    smile = VolatilitySmile(
        underlying="TEST",
        expiry=None,
        points=[
            VolatilityPoint(90.0, 0.30, OptionType.CALL),
            VolatilityPoint(100.0, 0.20, OptionType.CALL),
            VolatilityPoint(110.0, 0.25, OptionType.CALL),
        ],
    )

    k, w = calibration_data(
        smile,
        market,
        maturity,
    )

    assert len(k) == 3
    assert len(w) == 3

    expected = np.array([
        0.30**2,
        0.20**2,
        0.25**2,
    ]) * maturity

    assert np.allclose(
        w,
        expected,
    )


def test_objective_function_zero_for_true_parameters():
    params = SVIParameters(
        a=-0.05,
        b=0.30,
        rho=-0.40,
        m=0.00,
        sigma=0.20,
    )

    maturity = 0.10

    k = np.linspace(-0.5, 0.5, 40)

    observed_w = total_variance(
        k,
        params,
    )

    x = np.array([
        params.a,
        params.b,
        params.rho,
        params.m,
        params.sigma,
    ])

    value = objective_function(
        x,
        k,
        observed_w,
    )

    assert value < 1e-10


def test_calibrate_svi_recovers_smile():
    true = SVIParameters(
        a=-0.05,
        b=0.30,
        rho=-0.40,
        m=0.00,
        sigma=0.20,
    )

    maturity = 0.25

    market = MarketData(
        spot=100.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    forward = forward_price(
        market,
        maturity,
    )

    strikes = np.linspace(
        80,
        120,
        25,
    )

    points = []

    for strike in strikes:

        k = log_moneyness(
            strike,
            forward,
        )

        iv = implied_volatility(
            k,
            maturity,
            true,
        )

        points.append(
            VolatilityPoint(
                strike=strike,
                implied_volatility=iv,
                option_type=OptionType.CALL
            )
        )

    smile = VolatilitySmile(
        underlying="TEST",
        expiry=None,
        points=points,
    )

    fitted = calibrate_svi(
        smile,
        market,
        maturity,
    )

    fitted_iv = np.array([
        implied_volatility(
            log_moneyness(
                strike,
                forward,
            ),
            maturity,
            fitted,
        )
        for strike in strikes
    ])

    true_iv = np.array([
        implied_volatility(
            log_moneyness(
                strike,
                forward,
            ),
            maturity,
            true,
        )
        for strike in strikes
    ])

    rmse = np.sqrt(
        np.mean((fitted_iv - true_iv) ** 2)
    )

    assert rmse < 1e-2