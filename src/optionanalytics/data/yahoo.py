import yfinance as yf
import pandas as pd
from datetime import date

from ..models.option import OptionChain
from ..models.enums import OptionType
from ..models.option import OptionQuote


def _parse_quotes(df: pd.DataFrame, option_type: OptionType) -> list[OptionQuote]:
    """Parses a DataFrame of option quotes into a list of OptionQuote objects."""
    quotes = []
    for row in df.itertuples(index=False):
        volume = None if pd.isna(row.volume) else int(row.volume)
        quote = OptionQuote(
            option_type=option_type,
            strike=row.strike,
            bid=row.bid,
            ask=row.ask,
            last_price=row.lastPrice,
            volume=volume,
            open_interest=row.openInterest,
            last_trade_time=row.lastTradeDate,
        )
        quotes.append(quote)
    return quotes


def fetch_option_chain(ticker: str, expiry: str) -> OptionChain:
    """
    Fetches the option chain for a given ticker and expiry date from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol.
        expiry (str): The expiration date in 'YYYY-MM-DD' format.

    Returns:
        OptionChain: An object containing the option chain data.
    """
    ticker_data = yf.Ticker(ticker)
    raw_chain = ticker_data.option_chain(expiry)
    
    call_quotes = _parse_quotes(raw_chain.calls, OptionType.CALL)
    put_quotes = _parse_quotes(raw_chain.puts, OptionType.PUT)
    
    return OptionChain(
        underlying=ticker,
        expiry=date.fromisoformat(expiry),
        quotes=call_quotes + put_quotes
    )