import numpy as np

import config as cfg
from src.agent_factory import is_off_policy, is_rule_based, make_agent
from src.env import MultiUAVMECEnv


def _policy_mode(method):
    if method == "GreedyOffloading":
        return "greedy_offloading"
    if method == "LocalExecution":
        return "local_execution"
    return "learned"


def test_one_step_smoke_for_all_methods():
    domain = {
        "num_users": 9,
        "num_uavs": 3,
        "num_jammers": 0,
        "area_radius": 250,
        "wind_speed": 0.0,
    }

    for method in [
        "DMJO",
        "MAPPO",
        "MADDPG",
        "MATD3",
        "GreedyOffloading",
        "LocalExecution",
    ]:
        env = MultiUAVMECEnv(
            seed=11,
            domain_cfg=domain,
            policy_mode=_policy_mode(method),
            ablation_config=cfg.resolve_ablation("full"),
        )
        obs, state = env.reset()
        agent = make_agent(
            method,
            env.local_obs_dim,
            env.global_state_dim,
            env.agent_action_dim,
            env.n_agents,
            device="cpu",
        )

        actions, log_probs, values = agent.get_actions(
            obs, state, num_active=env.num_active)
        next_obs, next_state, rewards, done, info = env.step(actions)

        assert actions.shape == (env.n_agents, env.agent_action_dim)
        assert log_probs.shape == (env.n_agents,)
        assert values.shape == (env.n_agents,)
        assert next_obs.shape == obs.shape
        assert next_state.shape == state.shape
        assert np.isfinite(rewards).all()
        assert info["policy_mode"] == _policy_mode(method)


def test_method_classification_helpers():
    domain = {
        "num_users": 9,
        "num_uavs": 3,
        "num_jammers": 0,
        "area_radius": 250,
    }
    env = MultiUAVMECEnv(seed=12, domain_cfg=domain)

    expectations = {
        "DMJO": (False, False),
        "MAPPO": (False, False),
        "MADDPG": (True, False),
        "MATD3": (True, False),
        "GreedyOffloading": (False, True),
        "LocalExecution": (False, True),
    }

    for method, (off_policy, rule_based) in expectations.items():
        agent = make_agent(
            method,
            env.local_obs_dim,
            env.global_state_dim,
            env.agent_action_dim,
            env.n_agents,
            device="cpu",
        )
        assert is_off_policy(agent) is off_policy
        assert is_rule_based(agent) is rule_based
