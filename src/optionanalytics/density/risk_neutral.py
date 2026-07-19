from ..models.density import Density
from ..models.volatility import VolatilitySmile
from ..models.market import MarketData

def build_risk_neutral_density(smile: VolatilitySmile, market_data: MarketData) -> Density:
    pass