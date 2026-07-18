import pytest
from optionanalytics.models.market import MarketData

def test_create_valid_market_data():
    market_data = MarketData(spot=100.0, risk_free_rate=0.05, volatility=0.2)
    assert market_data.spot == 100.0
    assert market_data.risk_free_rate == 0.05
    assert market_data.volatility == 0.2

def test_negative_spot_raises_value_error():
    with pytest.raises(ValueError):
        MarketData(-100.0, 0.05, 0.2)

def test_zero_spot_raises_value_error():
    with pytest.raises(ValueError):
        MarketData(0.0, 0.05, 0.2)

def test_zero_volatility_raises_value_error():
    with pytest.raises(ValueError):
        MarketData(100.0, 0.05, 0.0)

def test_negative_volatility_raises_value_error():
    with pytest.raises(ValueError):
        MarketData(100.0, 0.05, -0.2)
