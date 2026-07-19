import pytest

from optionanalytics.models.volatility import VolatilitySurface

def test_empty_surface():
    with pytest.raises(ValueError):
        VolatilitySurface(
            underlying="AAPL",
            smiles=[],
        )

import datetime

from optionanalytics.models.enums import OptionType
from optionanalytics.models.volatility import (
    VolatilityPoint,
    VolatilitySmile,
)
from optionanalytics.volatility.surface import build_surface


def test_build_surface():
    smile1 = VolatilitySmile(
        underlying="AAPL",
        expiry=datetime.date(2026, 8, 21),
        points=[
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=320.0,
                implied_volatility=0.22,
            ),
            VolatilityPoint(
                option_type=OptionType.PUT,
                strike=320.0,
                implied_volatility=0.23,
            ),
        ],
    )

    smile2 = VolatilitySmile(
        underlying="AAPL",
        expiry=datetime.date(2026, 9, 18),
        points=[
            VolatilityPoint(
                option_type=OptionType.CALL,
                strike=320.0,
                implied_volatility=0.24,
            ),
            VolatilityPoint(
                option_type=OptionType.PUT,
                strike=320.0,
                implied_volatility=0.25,
            ),
        ],
    )

    surface = build_surface([smile1, smile2])

    assert surface.underlying == "AAPL"
    assert len(surface.smiles) == 2
    assert surface.smiles == [smile1, smile2]