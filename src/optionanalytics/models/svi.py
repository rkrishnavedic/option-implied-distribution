from dataclasses import dataclass


@dataclass
class SVIParameters:
    """
    Parameters of the raw SVI parameterization.

    The total implied variance is given by

        w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))

    where k is log-moneyness.
    """

    a: float
    b: float
    rho: float
    m: float
    sigma: float