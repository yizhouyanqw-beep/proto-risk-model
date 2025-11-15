from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class DeviceProfile:
    """
    Basic description of a prototype device.
    """
    device_id: str
    device_value: float      # monetary or relative value
    ip_sensitivity: float    # 0-1: how sensitive the IP is
    novelty: float           # 0-1: how new / non-public the technology is

@dataclass
class EnvironmentContext:
    """
    Context in which the device is currently operating.
    All values are in [0, 1] where 1 represents highest risk.
    """
    location_risk: float
    transit_risk: float
    operational_risk: float
    personnel_risk: float

@dataclass
class RiskFactorResult:
    """
    Result of a single factor computation.
    """
    name: str
    score: float             # 0-1
    details: Dict[str, Any]

@dataclass
class RiskScoreResult:
    """
    Final risk score in 0-100 scale, plus raw factor scores.
    """
    score_0_100: float
    factor_scores: Dict[str, float]
    attribution_pct: Dict[str, float]

@dataclass
class SimulationConfig:
    """
    Controls Monte Carlo simulation behavior.
    """
    n_paths: int = 1000
    location_volatility: float = 0.1
    transit_volatility: float = 0.1
    operational_volatility: float = 0.1
    personnel_volatility: float = 0.1

@dataclass
class SimulationResult:
    """
    Summary of Monte Carlo simulation.
    """
    mean_score: float
    p95_score: float
    path_scores: List[float]
