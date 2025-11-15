from typing import Dict
from .models import DeviceProfile, EnvironmentContext, RiskFactorResult

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def compute_device_value_factor(profile: DeviceProfile) -> RiskFactorResult:
    """
    Combine value, IP sensitivity, and novelty into a single device value factor.
    """
    # base: mostly driven by sensitivity + novelty
    base = 0.4 * profile.ip_sensitivity + 0.4 * profile.novelty

    # assume 100k is "very high" value, cap at 1.0
    value_scaled = min(profile.device_value / 100_000.0, 1.0)

    score = clamp01(base + 0.2 * value_scaled)

    return RiskFactorResult(
        name="device_value",
        score=score,
        details={
            "base": base,
            "value_scaled": value_scaled,
        },
    )

def compute_location_factor(ctx: EnvironmentContext) -> RiskFactorResult:
    score = clamp01(ctx.location_risk)
    return RiskFactorResult(
        name="location",
        score=score,
        details={"location_risk": ctx.location_risk},
    )

def compute_transit_factor(ctx: EnvironmentContext) -> RiskFactorResult:
    score = clamp01(ctx.transit_risk)
    return RiskFactorResult(
        name="transit",
        score=score,
        details={"transit_risk": ctx.transit_risk},
    )

def compute_operational_factor(ctx: EnvironmentContext) -> RiskFactorResult:
    score = clamp01(ctx.operational_risk)
    return RiskFactorResult(
        name="operational",
        score=score,
        details={"operational_risk": ctx.operational_risk},
    )

def compute_personnel_factor(ctx: EnvironmentContext) -> RiskFactorResult:
    score = clamp01(ctx.personnel_risk)
    return RiskFactorResult(
        name="personnel",
        score=score,
        details={"personnel_risk": ctx.personnel_risk},
    )

def compute_all_factors(
    profile: DeviceProfile,
    ctx: EnvironmentContext
) -> Dict[str, RiskFactorResult]:
    """
    Compute all primitive factors for a device in a given context.
    """
    factors = [
        compute_device_value_factor(profile),
        compute_location_factor(ctx),
        compute_transit_factor(ctx),
        compute_operational_factor(ctx),
        compute_personnel_factor(ctx),
    ]
    return {f.name: f for f in factors}
