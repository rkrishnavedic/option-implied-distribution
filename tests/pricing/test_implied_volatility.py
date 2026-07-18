from optionanalytics.models.enums import OptionType
from optionanalytics.models.option import EuropeanOption
from optionanalytics.models.market import MarketData
from optionanalytics.pricing.implied_volatility import implied_volatility

def test_implied_volatility_call():
    option_price = 10.0
    option = EuropeanOption(option_type=OptionType.CALL, strike=100.0, maturity=1.0)
    market_data = MarketData(spot=100.0, risk_free_rate=0.05, volatility=0.2)
    iv = implied_volatility(option_price, option, market_data)
    assert iv > 0

def test_implied_volatility_put():
    option_price = 10.0
    option = EuropeanOption(option_type=OptionType.PUT, strike=100.0, maturity=1.0)
    market_data = MarketData(spot=100.0, risk_free_rate=0.05, volatility=0.2)
    iv = implied_volatility(option_price, option, market_data)
    assert iv > 0