from ..models.volatility import VolatilitySmile, VolatilitySurface


def build_surface(smiles: list[VolatilitySmile]) -> VolatilitySurface:
    """
    Builds a volatility surface from a collection of volatility smiles.
    """
    if not smiles:
        raise ValueError("Cannot build a volatility surface from an empty list of smiles.")

    return VolatilitySurface(
        underlying=smiles[0].underlying,
        smiles=smiles,
    )