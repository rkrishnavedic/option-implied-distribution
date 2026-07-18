from optionanalytics.models.enums import OptionType
from optionanalytics.models.option import EuropeanOption
from optionanalytics.models.market import MarketData
from optionanalytics.pricing.black_scholes import black_scholes

def test_black_scholes_call():
    option = EuropeanOption(option_type=OptionType.CALL, strike=100.0, maturity=1.0)
    market_data = MarketData(spot=100.0, risk_free_rate=0.05, volatility=0.2)
    price = black_scholes(option, market_data)
    assert price > 0

def test_black_scholes_put():
    option = EuropeanOption(option_type=OptionType.PUT, strike=100.0, maturity=1.0)
    market_data = MarketData(spot=100.0, risk_free_rate=0.05, volatility=0.2)
    price = black_scholes(option, market_data)
    assert price > 0