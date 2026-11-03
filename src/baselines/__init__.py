"""Backward-compatibility shim for dmjo_mec.baselines."""
from dmjo_mec.baselines import *
from dmjo_mec.baselines.mappo_baseline import MAPPOBaseline
from dmjo_mec.baselines.maddpg_agent import MADDPGAgent
from dmjo_mec.baselines.matd3_agent import MATD3Agent
from dmjo_mec.baselines.greedy_agent import GreedyOffloadingAgent
from dmjo_mec.baselines.local_agent import LocalExecutionAgent
