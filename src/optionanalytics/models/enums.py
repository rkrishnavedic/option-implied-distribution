from enum import StrEnum


class OptionType(StrEnum):
    CALL = "call"
    PUT = "put"

class InterpolationMethod(StrEnum):
    CUBIC_SPLINE = "cubic_spline"
    PCHIP = "pchip"
    AKIMA = "akima"