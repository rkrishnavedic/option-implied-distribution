import pandas as pd

from optionanalytics.data.yahoo import _parse_quotes
from optionanalytics.models.enums import OptionType

import pytest
import yfinance as yf

from optionanalytics.data.yahoo import fetch_option_chain



def test_parse_quotes_creates_option_quotes():
    df = pd.DataFrame(
        [
            {
                "strike": 100.0,
                "bid": 5.0,
                "ask": 5.5,
                "lastPrice": 5.25,
                "volume": 10,
                "openInterest": 25,
                "lastTradeDate": pd.Timestamp("2026-07-18T10:00:00Z"),
            }
        ]
    )

    quotes = _parse_quotes(df, OptionType.CALL)

    assert len(quotes) == 1

    quote = quotes[0]

    assert quote.option_type == OptionType.CALL
    assert quote.strike == 100.0
    assert quote.bid == 5.0
    assert quote.ask == 5.5
    assert quote.last_price == 5.25
    assert quote.volume == 10
    assert quote.open_interest == 25
    assert quote.last_trade_time == pd.Timestamp("2026-07-18T10:00:00Z")

def test_parse_quotes_handles_missing_volume():
    df = pd.DataFrame(
        [
            {
                "strike": 100.0,
                "bid": 5.0,
                "ask": 5.5,
                "lastPrice": 5.25,
                "volume": float("nan"),
                "openInterest": 25,
                "lastTradeDate": pd.Timestamp("2026-07-18T10:00:00Z"),
            }
        ]
    )

    quote = _parse_quotes(df, OptionType.PUT)[0]

    assert quote.volume is None

@pytest.mark.integration
def test_fetch_option_chain():
    ticker = yf.Ticker("AAPL")
    expiry = ticker.options[0]

    chain = fetch_option_chain("AAPL", expiry)

    assert chain.underlying == "AAPL"
    assert chain.expiry == expiry
    assert len(chain.quotes) > 0