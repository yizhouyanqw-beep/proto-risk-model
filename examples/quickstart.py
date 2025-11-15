"""
Quickstart example for proto_risk_model.

Usage:
    python -m examples.quickstart
(or adjust PYTHONPATH to include project root)
"""

from pprint import pprint
from proto_risk_model import (
    DeviceProfile,
    EnvironmentContext,
    SimulationConfig,
    evaluate_risk,
    simulate_risk,
)

def main() -> None:
    profile = DeviceProfile(
        device_id="prototype-camera-v3",
        device_value=80_000,
        ip_sensitivity=0.85,
        novelty=0.9,
    )

    ctx = EnvironmentContext(
        location_risk=0.4,
        transit_risk=0.7,
        operational_risk=0.3,
        personnel_risk=0.5,
    )

    # 1) Deterministic risk evaluation
    result = evaluate_risk(profile, ctx)
    print("=== Deterministic Risk ===")
    print(f"Score: {result.score_0_100:.2f} / 100")
    print("Factor scores:")
    pprint(result.factor_scores)
    print("Attribution (%):")
    pprint(result.attribution_pct)
    print()

    # 2) Monte Carlo simulation
    sim_cfg = SimulationConfig(
        n_paths=2000,
        location_volatility=0.08,
        transit_volatility=0.12,
        operational_volatility=0.08,
        personnel_volatility=0.1,
    )

    sim_result = simulate_risk(profile, ctx, config=sim_cfg)
    print("=== Monte Carlo Simulation ===")
    print(f"Mean score: {sim_result.mean_score:.2f}")
    print(f"95th percentile: {sim_result.p95_score:.2f}")
    print(f"Paths: {len(sim_result.path_scores)}")

if __name__ == "__main__":
    main()
