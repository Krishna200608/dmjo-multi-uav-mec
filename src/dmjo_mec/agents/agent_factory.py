"""
Agent Factory - single-point model switcher
===============================================
Change METHOD below (or pass --method on the CLI) to run any of the
comparison methods without touching train.py.

Supported methods
-----------------
  "MAPPO"           - MAPPO-based joint MEC optimization (ours)
  "DMJO"            - backward-compatible alias for MAPPO
  "MADDPG"          - deterministic multi-agent actor-critic baseline
  "MATD3"           - double-Q deterministic MARL baseline
  "GreedyOffloading"- nearest-UAV, cache-unaware baseline
  "LocalExecution"  - all tasks local at WD baseline

Quick usage in train.py
-----------------------
    from dmjo_mec.agents.agent_factory import make_agent, METHOD

    agent = make_agent(
        method     = METHOD,          # or pass args.method
        obs_dim    = env.local_obs_dim,
        state_dim  = env.global_state_dim,
        action_dim = env.agent_action_dim,
        n_agents   = env.n_agents,
        device     = device,
    )

CLI integration (add to train.py argparse):
-------------------------------------------
    parser.add_argument('--method', default='MAPPO',
        choices=['DMJO','MAPPO','MADDPG','MATD3',
                 'GreedyOffloading','LocalExecution'],
        help='Training/evaluation method')

Notes
-----
* MADDPG / MATD3 are off-policy. Their update() call uses an internal
  replay buffer that is filled by calling agent.push_transition() once
  per env step (add this call alongside buffer.insert() in train.py).

* GreedyOffloading and LocalExecution are rule-based. Their update()
  is a no-op and their save()/load() write/read a small JSON metadata
  file (no model weights).

* All agents expose the identical interface:
      get_actions(obs, state, num_active) -> actions, log_probs, values
      get_values(state)                   -> values
      update(buffer)                      -> metrics dict
      save(path) / load(path)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ================================================================
# CHANGE THIS LINE TO SWITCH MODELS
# ================================================================
METHOD = "MAPPO"
# ================================================================
# Choices: "DMJO" | "MAPPO" | "MADDPG" | "MATD3"
#        | "GreedyOffloading" | "LocalExecution"
# ================================================================


def make_agent(method: str, obs_dim: int, state_dim: int,
               action_dim: int, n_agents: int,
               device: str = "cpu", **kwargs):
    """
    Instantiate and return the requested agent.

    Parameters
    ----------
    method      : one of the METHOD strings listed above
    obs_dim     : local observation dimension  (env.local_obs_dim)
    state_dim   : global state dimension       (env.global_state_dim)
    action_dim  : per-agent action dimension   (env.agent_action_dim)
    n_agents    : number of UAV agents         (env.n_agents)
    device      : torch device string          ("cpu" or "cuda")
    **kwargs    : forwarded to agent __init__  (e.g. share_actor=False)

    Returns
    -------
    agent object with the standard interface described above.
    """
    m = method.strip()

    if m in {"MAPPO", "DMJO"}:
        # MAPPO is the final claimed method. DMJO is kept as a legacy alias
        # for old commands/checkpoint folder names and runs the same policy.
        from dmjo_mec.agents.mappo_agent import MAPPOAgent
        return MAPPOAgent(obs_dim, state_dim, action_dim, n_agents,
                          device=device, **kwargs)

    elif m == "MADDPG":
        # Deterministic MARL baseline.
        from dmjo_mec.baselines.maddpg_agent import MADDPGAgent
        return MADDPGAgent(obs_dim, state_dim, action_dim, n_agents,
                           device=device, **kwargs)

    elif m == "MATD3":
        # Double-Q deterministic MARL baseline.
        from dmjo_mec.baselines.matd3_agent import MATD3Agent
        return MATD3Agent(obs_dim, state_dim, action_dim, n_agents,
                          device=device, **kwargs)

    elif m == "GreedyOffloading":
        # Nearest-UAV greedy rule baseline.
        from dmjo_mec.baselines.greedy_agent import GreedyOffloadingAgent
        return GreedyOffloadingAgent(obs_dim, state_dim, action_dim,
                                     n_agents, device=device, **kwargs)

    elif m == "LocalExecution":
        # All tasks computed locally.
        from dmjo_mec.baselines.local_agent import LocalExecutionAgent
        return LocalExecutionAgent(obs_dim, state_dim, action_dim,
                                   n_agents, device=device, **kwargs)

    else:
        valid = ("DMJO", "MAPPO", "MADDPG", "MATD3",
                 "GreedyOffloading", "LocalExecution")
        raise ValueError(
            f"Unknown method '{m}'. Choose from: {valid}"
        )


# ================================================================
# Off-policy helper
# ================================================================
def is_off_policy(agent) -> bool:
    """
    Returns True for MADDPG / MATD3 agents that need push_transition().
    Use this guard in train.py to add the replay-push call:

        if is_off_policy(agent):
            agent.push_transition(obs, state, actions, rewards,
                                  next_obs, next_state, done)
    """
    return hasattr(agent, 'push_transition')


def is_rule_based(agent) -> bool:
    """
    Returns True for GreedyOffloading and LocalExecution (no training).
    Use this to skip the update() call if you want to save time:

        if not is_rule_based(agent):
            metrics = agent.update(buffer)
    """
    return getattr(agent, 'METHOD', None) in {"GreedyOffloading", "LocalExecution"}


# ================================================================
# Pretty summary
# ================================================================
_METHOD_DESCRIPTIONS = {
    "MAPPO":            "MAPPO-based joint offloading, caching, trajectory, and NOMA (ours)",
    "DMJO":             "Legacy alias for MAPPO; no diffusion is used",
    "MADDPG":           "Deterministic multi-agent actor-critic baseline",
    "MATD3":            "Double-Q deterministic multi-agent DRL baseline",
    "GreedyOffloading": "Nearest-UAV association without caching awareness",
    "LocalExecution":   "All tasks executed locally at WDs",
}


def describe(method: str) -> str:
    return _METHOD_DESCRIPTIONS.get(method, "Unknown method")


if __name__ == "__main__":
    print("Available methods (Table I):\n")
    for no, (k, v) in enumerate(_METHOD_DESCRIPTIONS.items(), 1):
        marker = " <- active" if k == METHOD else ""
        print(f"  {no}. {k:<20s}  {v}{marker}")
    print(f"\nTo switch: edit METHOD = '...' in src/agent_factory.py")
    print(f"           or pass --method <name> on the CLI")
