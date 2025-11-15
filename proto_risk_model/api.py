from typing import Dict, Optional
from .models import (
    DeviceProfile,
    EnvironmentContext,
    RiskScoreResult,
    SimulationConfig,
    SimulationResult,
)
from .config import DEFAULT_WEIGHTS
from .factors import compute_all_factors
from .scoring import compute_risk_score
from .simulator import run_monte_carlo

def evaluate_risk(
    profile: DeviceProfile,
    context: EnvironmentContext,
    weights: Optional[Dict[str, float]] = None,
) -> RiskScoreResult:
    """
    High-level API: compute deterministic risk score for a device.
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    factors = compute_all_factors(profile, context)
    return compute_risk_score(factors, weights)

def simulate_risk(
    profile: DeviceProfile,
    context: EnvironmentContext,
    weights: Optional[Dict[str, float]] = None,
    config: Optional[SimulationConfig] = None,
) -> SimulationResult:
    """
    High-level API: Monte Carlo simulation of risk scores.
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    return run_monte_carlo(profile, context, weights, config)

def explain_risk(
    profile: DeviceProfile,
    context: EnvironmentContext,
    weights: Optional[Dict[str, float]] = None,
) -> RiskScoreResult:
    """
    Same as evaluate_risk, but semantically used when you want attribution.
    (RiskScoreResult already contains attribution_pct.)
    """
    return evaluate_risk(profile, context, weights)
