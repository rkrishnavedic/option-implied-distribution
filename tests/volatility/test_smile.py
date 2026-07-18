import datetime
from freezegun import freeze_time

from optionanalytics.models.enums import OptionType
from optionanalytics.models.market import MarketData
from optionanalytics.models.option import OptionChain, OptionQuote, EuropeanOption
from optionanalytics.pricing.black_scholes import black_scholes
from optionanalytics.volatility.smile import build_smile

@freeze_time("2026-07-18 14:09:00.000")
def test_build_smile():
    market_data = MarketData(
        spot=100.0,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    expiry = datetime.date(2027,7,18)

    option = EuropeanOption(
        option_type=OptionType.CALL,
        strike=100.0,
        maturity=1.0,
    )

    price = black_scholes(option, market_data)

    quote = OptionQuote(
        option_type=OptionType.CALL,
        strike=100.0,
        bid=price,
        ask=price,
        last_price=price,
        volume=100,
        open_interest=100,
        last_trade_time=datetime.datetime.now(),
    )

    chain = OptionChain(
        underlying="TEST",
        expiry=expiry,
        quotes=[quote],
    )

    smile = build_smile(chain, market_data, datetime.date.today())

    assert len(smile.points) == 1

    point = smile.points[0]

    assert point.strike == 100.0
    assert abs(point.implied_volatility - 0.20) < 1e-6