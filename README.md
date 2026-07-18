# Option-Implied Risk-Neutral Distribution Analytics

A quantitative finance library for recovering, validating, and analyzing option-implied risk-neutral probability distributions from listed option prices.

## Objectives

- Recover option-implied risk-neutral probability distributions
- Develop a robust option analytics pipeline
- Validate recovered distributions using financial theory and numerical methods
- Build production-quality, modular quantitative finance software

## Roadmap

- [ ] Black-Scholes pricing
- [ ] Implied volatility solver
- [ ] Option chain ingestion
- [ ] Data cleaning
- [ ] Static arbitrage checks
- [ ] Implied volatility smile construction (single expiry)
- [ ] Arbitrage-free volatility surface calibration (multiple expiries)
- [ ] Risk-neutral density recovery
- [ ] Distribution analytics
- [ ] Visualization
- [ ] Documentation

## Repository Structure

```
src/
tests/
notebooks/
docs/
```

---

🚧 **Status:** Project planning and design.

---
### Setup Notes
#### Install dependencies
`poetry install`

#### View env info
`poetry env info`

#### Add dependency
`poetry add numpy`

#### Add dev dependency
`poetry add --group dev pytest`

#### Open shell
`poetry shell`

#### Run script
`poetry run python script.py`

#### Run tests
`poetry run pytest`

#### Adding dev dependencies
`poetry add --group dev jupyterlab ipykernel`