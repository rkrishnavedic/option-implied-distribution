![Build](https://github.com/rkrishnavedic/option-implied-distribution/actions/workflows/tests.yml/badge.svg)

# Option-Implied Risk-Neutral Distribution Analytics

A quantitative finance library for constructing implied volatility smiles and surfaces, recovering risk-neutral probability distributions from option prices, and validating numerical methods used in option analytics.

## Features

- Black-Scholes option pricing
- Implied volatility solver
- Yahoo Finance option chain ingestion
- Option quote cleaning and validation
- Static arbitrage checks
- Implied volatility smile construction
- Volatility surface construction
- Multiple smile interpolation methods
  - PCHIP
  - Akima
  - Cubic Spline
- Breeden–Litzenberger risk-neutral density extraction
- Numerical validation notebooks
- Comprehensive unit test suite

## Numerical Validation

The density extraction implementation has been validated under a constant-volatility Black-Scholes model.

A controlled experiment showed that:

- Constant volatility recovers a smooth density with total probability ≈ **1.000000**
- Generic smile interpolation (PCHIP, Akima and Cubic Spline) produces unstable second derivatives, leading to densities whose total probability exceeds one

This demonstrates that the numerical differentiation pipeline is correct, while highlighting the need for arbitrage-aware volatility parameterizations for stable density recovery.

## Roadmap

### Phase 1 — Prototype ✅

- [x] Black-Scholes pricing
- [x] Implied volatility solver
- [x] Option chain ingestion
- [x] Data cleaning
- [x] Static arbitrage validation
- [x] Implied volatility smile construction
- [x] Volatility surface construction
- [x] Smile interpolation
- [x] Breeden–Litzenberger density extraction
- [x] Numerical validation

### Phase 2 — Research

- [ ] SVI volatility smile calibration
- [ ] Arbitrage-free volatility surface
- [ ] Stable risk-neutral density extraction
- [ ] Distribution analytics
- [ ] Density moments (mean, variance, skewness, kurtosis)
- [ ] Local volatility extraction
- [ ] Interactive visualizations
- [ ] Documentation website

## Repository Structure

```text
src/
tests/
notebooks/
docs/
```

## Current Status

**Version:** Prototype Complete (v1)

The core option analytics pipeline has been implemented and validated.
Current research focuses on replacing generic smile interpolation with arbitrage-aware parameterizations (SVI) for stable market-implied density recovery.

---

## Development

### Install dependencies

```bash
poetry install
```

### Activate environment

```bash
poetry shell
```

### Run tests

```bash
poetry run pytest
```

### Run notebooks

```bash
poetry run jupyter lab
```

### Add dependency

```bash
poetry add <package>
```

### Add development dependency

```bash
poetry add --group dev <package>
```