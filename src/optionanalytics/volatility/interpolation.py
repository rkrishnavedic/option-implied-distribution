from collections import defaultdict
from collections.abc import Callable

from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator

from ..models.volatility import VolatilitySmile
from ..models.enums import InterpolationMethod


def interpolate_smile(
        smile: VolatilitySmile, 
        method: InterpolationMethod = InterpolationMethod.PCHIP
    ) -> Callable[[float], float]:
    grouped = defaultdict(list)

    for point in smile.points:
        grouped[point.strike].append(point.implied_volatility)

    strikes = sorted(grouped)

    vols = [
        sum(grouped[strike]) / len(grouped[strike])
        for strike in strikes
    ]

    match method:
        case InterpolationMethod.CUBIC_SPLINE: 
            return CubicSpline(strikes, vols)
        
        case InterpolationMethod.PCHIP: 
            return PchipInterpolator(strikes, vols)
        
        case InterpolationMethod.AKIMA: 
            return Akima1DInterpolator(strikes, vols)
        
        case _: 
            raise ValueError(f"Unsupported interpolation method: {method}")