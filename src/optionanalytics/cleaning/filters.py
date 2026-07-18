from ..models.option import OptionQuote, OptionChain

def _remove_zero_ask(quotes: list[OptionQuote]) -> list[OptionQuote]:
    """Removes quotes with zero ask price."""
    return [quote for quote in quotes if quote.ask > 0]

def _remove_zero_open_interest(quotes: list[OptionQuote]) -> list[OptionQuote]:
    """Removes quotes with zero open interest."""
    return [quote for quote in quotes if quote.open_interest > 0]

def _remove_crossed_quotes(quotes: list[OptionQuote]) -> list[OptionQuote]:
    """Removes quotes where the bid is greater than the ask."""
    return [quote for quote in quotes if quote.bid <= quote.ask]

def clean_option_chain(option_chain: OptionChain) -> OptionChain:
    """Cleans an option chain by removing invalid quotes."""
    quotes = option_chain.quotes

    quotes = _remove_zero_ask(quotes)
    quotes = _remove_zero_open_interest(quotes)
    quotes = _remove_crossed_quotes(quotes)

    return OptionChain(
        underlying=option_chain.underlying,
        expiry=option_chain.expiry,
        quotes=quotes
    )