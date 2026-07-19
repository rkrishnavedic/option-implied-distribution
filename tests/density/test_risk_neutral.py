import datetime

from optionanalytics.density.risk_neutral import build_density
from optionanalytics.models.density import Density
from optionanalytics.models.enums import OptionType
from optionanalytics.models.market import MarketData
from optionanalytics.models.option import OptionQuote
from optionanalytics.models.volatility import VolatilityPoint, VolatilitySmile


def test_build_density():
    smile = VolatilitySmile(
        underlying="AAPL",
        expiry=datetime.date(2026, 8, 21),
        points=[
            VolatilityPoint(
                strike=90.0,
                implied_volatility=0.30,
                option_type=OptionType.CALL,
            ),
            VolatilityPoint(
                strike=100.0,
                implied_volatility=0.25,
                option_type=OptionType.CALL,
            ),
            VolatilityPoint(
                strike=110.0,
                implied_volatility=0.28,
                option_type=OptionType.CALL,
            ),
        ],
    )

    market = MarketData(
        spot=100.0,
        risk_free_rate=0.05,
        volatility=0.20,  # ignored
    )

    valuation_date = datetime.date(2026, 7, 21)

    density = build_density(
        smile=smile,
        market_data=market,
        valuation_date=valuation_date,
    )

    assert isinstance(density, Density)
    assert density.underlying == "AAPL"
    assert density.expiry == datetime.date(2026, 8, 21)

    assert len(density.points) > 0

    for point in density.points:
        assert point.strike > 0
        assert point.probability_density >= 0