import random
from typing import Dict, List, Optional

from .models import (
    DeviceProfile,
    EnvironmentContext,
    SimulationConfig,
    SimulationResult,
)
from .factors import compute_all_factors
from .scoring import compute_risk_score

def _perturb(value: float, volatility: float) -> float:
    """
    Simple normal-like perturbation with clipping to [0,1].
    """
    shock = random.gauss(0, volatility)
    return min(1.0, max(0.0, value + shock))


def run_monte_carlo(
    profile: DeviceProfile,
    base_ctx: EnvironmentContext,
    weights: Dict[str, float],
    config: Optional[SimulationConfig] = None,
) -> SimulationResult:
    """
    Run Monte Carlo simulation of lifecycle risk scores by perturbing the context.
    """
    if config is None:
        config = SimulationConfig()

    scores: List[float] = []

    for _ in range(config.n_paths):
        sim_ctx = EnvironmentContext(
            location_risk=_perturb(base_ctx.location_risk, config.location_volatility),
            transit_risk=_perturb(base_ctx.transit_risk, config.transit_volatility),
            operational_risk=_perturb(base_ctx.operational_risk, config.operational_volatility),
            personnel_risk=_perturb(base_ctx.personnel_risk, config.personnel_volatility),
        )

        factors = compute_all_factors(profile, sim_ctx)
        result = compute_risk_score(factors, weights)
        scores.append(result.score_0_100)

    sorted_scores = sorted(scores)
    idx_p95 = int(0.95 * len(sorted_scores)) - 1
    idx_p95 = max(0, min(idx_p95, len(sorted_scores) - 1))

    mean_score = sum(sorted_scores) / len(sorted_scores)
    p95_score = sorted_scores[idx_p95]

    return SimulationResult(
        mean_score=mean_score,
        p95_score=p95_score,
        path_scores=scores,
    )
