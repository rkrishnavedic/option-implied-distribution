from collections import defaultdict

from scipy.interpolate import CubicSpline

from ..models.volatility import VolatilitySmile


def interpolate_smile(smile: VolatilitySmile):
    grouped = defaultdict(list)

    for point in smile.points:
        grouped[point.strike].append(point.implied_volatility)

    strikes = sorted(grouped)

    vols = [
        sum(grouped[strike]) / len(grouped[strike])
        for strike in strikes
    ]

    return CubicSpline(strikes, vols)