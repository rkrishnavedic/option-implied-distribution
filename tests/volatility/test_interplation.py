import datetime

import pytest

from optionanalytics.models.enums import OptionType
from optionanalytics.models.volatility import VolatilityPoint,VolatilitySmile
from optionanalytics.volatility.interpolation import interpolate_smile


@pytest.fixture
def smile():
    return VolatilitySmile(
        underlying="AAPL",
        expiry=datetime.date(2026, 8, 21),
        points=[
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=100.0,
                implied_volatility=0.20,
            ),
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=110.0,
                implied_volatility=0.22,
            ),
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=120.0,
                implied_volatility=0.25,
            ),
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=130.0,
                implied_volatility=0.24,
            ),
        ],
    )


def test_interpolate_smile_returns_callable(smile):
    interpolator = interpolate_smile(smile)

    assert callable(interpolator)


def test_interpolates_known_points(smile):
    interpolator = interpolate_smile(smile)

    assert interpolator(100.0) == pytest.approx(0.20)
    assert interpolator(110.0) == pytest.approx(0.22)
    assert interpolator(120.0) == pytest.approx(0.25)
    assert interpolator(130.0) == pytest.approx(0.24)


def test_interpolates_between_points(smile):
    interpolator = interpolate_smile(smile)

    iv = interpolator(115.0)

    assert 0.22 < iv < 0.25


def test_duplicate_strikes_are_averaged():
    smile = VolatilitySmile(
        underlying="AAPL",
        expiry=datetime.date(2026, 8, 21),
        points=[
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=100.0,
                implied_volatility=0.20,
            ),
            VolatilityPoint(
                option_type=OptionType.PUT,
                strike=100.0,
                implied_volatility=0.22,
            ),
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=110.0,
                implied_volatility=0.25,
            ),
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=120.0,
                implied_volatility=0.28,
            ),
        ],
    )

    interpolator = interpolate_smile(smile)

    assert interpolator(100.0) == pytest.approx(0.21)