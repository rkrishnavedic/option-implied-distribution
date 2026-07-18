from scipy.stats import norm

def normal_cdf(x: float) -> float:
    return norm.cdf(x)

def normal_pdf(x: float) -> float:
    return norm.pdf(x)