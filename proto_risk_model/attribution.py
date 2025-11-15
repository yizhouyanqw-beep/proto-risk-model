from typing import Dict

from .models import RiskFactorResult

def _normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """
    Local copy of weight normalization to avoid circular import with scoring.
    """
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weight sum must be positive")
    return {k: v / total for k, v in weights.items()}

def compute_attribution(
    factors: Dict[str, RiskFactorResult],
    weights: Dict[str, float],
) -> Dict[str, float]:
    """
    Compute simple percentage attribution of each factor to the final score.

    Returns a mapping from factor name to percentage (0-100).
    """
    norm_w = _normalize_weights(weights)

    contributions: Dict[str, float] = {}
    total_contribution = 0.0

    for name, factor in factors.items():
        w = norm_w.get(name, 0.0)
        contrib = w * factor.score
        contributions[name] = contrib
        total_contribution += contrib

    if total_contribution <= 0:
        return {k: 0.0 for k in contributions.keys()}

    return {
        k: (v / total_contribution) * 100.0
        for k, v in contributions.items()
    }
