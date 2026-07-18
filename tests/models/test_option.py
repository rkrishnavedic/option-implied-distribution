import pytest
from optionanalytics.models.enums import OptionType
from optionanalytics.models.option import EuropeanOption

def test_create_valid_european_option():
    option = EuropeanOption(
        option_type=OptionType.CALL,
        strike=100.0,
        maturity=1.0,
    )
    assert option.option_type == OptionType.CALL
    assert option.strike == 100.0
    assert option.maturity == 1.0

def test_negative_strike_raises_value_error():
    with pytest.raises(ValueError):
        EuropeanOption(OptionType.PUT, -100.0, 1.0)

def test_zero_maturity_raises_value_error():
    with pytest.raises(ValueError):
        EuropeanOption(OptionType.CALL, 100.0, 0.0)

def test_zero_strike_raises_value_error():
    with pytest.raises(ValueError):
        EuropeanOption(OptionType.PUT, 0.0, 1.0)

def test_negative_maturity_raises_value_error():
    with pytest.raises(ValueError):
        EuropeanOption(OptionType.CALL, 100.0, -1.0)