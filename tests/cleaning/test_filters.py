from datetime import datetime, UTC

from optionanalytics.cleaning.filters import clean_option_chain
from optionanalytics.models.enums import OptionType
from optionanalytics.models.option import OptionChain, OptionQuote


def test_remove_zero_ask_quotes():
    valid_quote = OptionQuote(
        option_type=OptionType.CALL,
        strike=100.0,
        bid=5.0,
        ask=5.5,
        last_price=5.2,
        volume=10,
        open_interest=100,
        last_trade_time=datetime.now(UTC),
    )

    invalid_quote = OptionQuote(
        option_type=OptionType.CALL,
        strike=105.0,
        bid=0.0,
        ask=0.0,
        last_price=0.0,
        volume=5,
        open_interest=50,
        last_trade_time=datetime.now(UTC),
    )

    chain = OptionChain(
        underlying="AAPL",
        expiry="2026-07-24",
        quotes=[valid_quote, invalid_quote],
    )

    cleaned = clean_option_chain(chain)

    assert len(cleaned.quotes) == 1
    assert cleaned.quotes[0] == valid_quote

def test_clean_option_chain_returns_empty_quotes_when_all_removed():
    quote = OptionQuote(
        option_type=OptionType.CALL,
        strike=100.0,
        bid=0.0,
        ask=0.0,
        last_price=0.0,
        volume=10,
        open_interest=50,
        last_trade_time=datetime.now(UTC),
    )

    chain = OptionChain(
        underlying="AAPL",
        expiry="2026-07-24",
        quotes=[quote],
    )

    cleaned = clean_option_chain(chain)

    assert cleaned.quotes == []