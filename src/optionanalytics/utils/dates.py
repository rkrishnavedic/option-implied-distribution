from datetime import date

def year_fraction(expiry: date, valuation_date: date) -> float:
    return (expiry - valuation_date).days/365.0