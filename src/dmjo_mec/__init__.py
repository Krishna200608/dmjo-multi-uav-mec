"""
DMJO-MEC: Priority-Aware Multi-UAV Mobile Edge Computing
=========================================================
Multi-Agent Reinforcement Learning framework with MAPPO,
Centralized Training with Decentralized Execution (CTDE),
elevation-dependent Air-to-Ground channel models, analytical NOMA power bisection,
cooperative edge service caching, and 3D rotary-wing aerodynamics.
"""

__version__ = "1.0.0"

from dmjo_mec.environment.env import MultiUAVMECEnv, DomainRandomiser
from dmjo_mec.agents.mappo_agent import MAPPOAgent
from dmjo_mec.agents.agent_factory import make_agent, describe
from dmjo_mec import config

__all__ = [
    "MultiUAVMECEnv",
    "DomainRandomiser",
    "MAPPOAgent",
    "make_agent",
    "describe",
    "config",
    "__version__",
]
