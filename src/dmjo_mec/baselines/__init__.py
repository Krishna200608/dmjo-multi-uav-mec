"""Baseline agents for comparison against the primary MAPPO framework."""
from dmjo_mec.baselines.mappo_baseline import MAPPOBaseline
from dmjo_mec.baselines.maddpg_agent import MADDPGAgent
from dmjo_mec.baselines.matd3_agent import MATD3Agent
from dmjo_mec.baselines.greedy_agent import GreedyOffloadingAgent
from dmjo_mec.baselines.local_agent import LocalExecutionAgent

__all__ = [
    "MAPPOBaseline",
    "MADDPGAgent",
    "MATD3Agent",
    "GreedyOffloadingAgent",
    "LocalExecutionAgent",
]
