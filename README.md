# proto-risk-model
A lightweight, simulation-driven risk-scoring framework for prototype device security

## Overview

proto_risk_model is a lightweight Python package that applies financial engineering–style factor modeling, Monte-Carlo simulation, and risk attribution techniques to evaluate the security exposure of hardware prototype devices across their lifecycle.

This framework quantifies risk for:

Early-stage engineering prototypes

Supply-chain transitions

Demo units and field test devices

High-sensitivity hardware containing proprietary IP

The model is designed to support IP protection, hardware governance, supply-chain security, and operational risk evaluation — areas increasingly critical for large-scale device companies and national-interest domains.

## Key Capabilities

### Factor-based risk scoring
The model decomposes risk into five interpretable dimensions:

- Device Value Factor — IP sensitivity, novelty, market impact

- Location Factor — factory/site/geopolitical risk

- Transit Factor — shipping & logistics volatility

- Operational Factor — process control and chain-of-custody gaps

- Personnel Factor — access-control and insider risk

### Monte Carlo lifecycle simulation
Simulates thousands of potential security-exposure scenarios by perturbing environmental volatility, producing:

- Mean expected risk

- Tail exposure risk (e.g., 95th percentile)

- Distribution analysis for “worst-case” outcomes

### Risk attribution
Breaks down the final risk score into percentage contributions from each factor — similar to FE-style factor attribution.

### Configurable, modular, reproducible
- Pure Python

- No cloud dependencies

- Highly extensible factor architecture

- Designed for integration with Jupyter/Colab/Codespaces workflows

## Package Installation
Clone the repository:
```
git clone https://github.com/yourname/proto-risk-model.git
cd proto-risk-model
```
Install in editable mode:
```
pip install -e .
```

## Quickstart Example
```
from proto_risk_model import (
    DeviceProfile,
    EnvironmentContext,
    evaluate_risk,
    simulate_risk,
    SimulationConfig,
)

profile = DeviceProfile(
    device_id="prototype-camera-v3",
    device_value=80000,
    ip_sensitivity=0.85,
    novelty=0.9,
)

context = EnvironmentContext(
    location_risk=0.4,
    transit_risk=0.7,
    operational_risk=0.3,
    personnel_risk=0.5,
)

# Deterministic evaluation
result = evaluate_risk(profile, context)
print("Risk Score:", result.score_0_100)
print("Factor Scores:", result.factor_scores)
print("Attribution (%):", result.attribution_pct)

# Monte-Carlo simulation
cfg = SimulationConfig(n_paths=2000)
sim_result = simulate_risk(profile, context, config=cfg)
print("Mean:", sim_result.mean_score)
print("P95:", sim_result.p95_score)
```

## Model Architecture
```
proto_risk_model/
│
├── models.py          # Dataclasses for profiles, context, results
├── factors.py         # Factor computations
├── scoring.py         # Weighted scoring + factor aggregation
├── attribution.py     # Risk attribution decomposition
├── simulator.py       # Monte Carlo lifecycle simulation
├── api.py             # Friendly high-level API (evaluate_risk, simulate_risk)
└── config.py          # Default factor weighting
```

