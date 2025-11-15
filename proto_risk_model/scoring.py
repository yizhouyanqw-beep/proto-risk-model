from typing import Dict

from .models import RiskFactorResult, RiskScoreResult
from .attribution import compute_attribution

def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize raw factor weights to sum to 1.0.
    """
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weight sum must be positive")
    return {k: v / total for k, v in weights.items()}

def compute_risk_score(
    factors: Dict[str, RiskFactorResult],
    weights: Dict[str, float],
) -> RiskScoreResult:
    """
    Compute a 0-100 risk score given factor results and weights.
    """
    norm_w = normalize_weights(weights)
    score_0_1 = 0.0
    factor_scores: Dict[str, float] = {}

    for name, factor in factors.items():
        w = norm_w.get(name, 0.0)
        contribution = w * factor.score
        score_0_1 += contribution
        factor_scores[name] = factor.score

    attribution_pct = compute_attribution(factors, weights)

    return RiskScoreResult(
        score_0_100=score_0_1 * 100.0,
        factor_scores=factor_scores,
        attribution_pct=attribution_pct,
    )
