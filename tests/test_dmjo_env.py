import numpy as np

import config as cfg
from src.agent_factory import make_agent
from src.diffusion import GaussianOnlyActor
from src.env import MultiUAVMECEnv


def small_domain(num_users=12, num_uavs=3, num_jammers=0):
    return {
        "num_users": num_users,
        "num_uavs": num_uavs,
        "num_jammers": num_jammers,
        "area_radius": 300,
        "wind_speed": 0.0,
    }


def test_env_reset_step_shapes_and_finite_rewards():
    env = MultiUAVMECEnv(seed=1, domain_cfg=small_domain())
    obs, state = env.reset()
    actions = np.zeros((env.n_agents, env.agent_action_dim), dtype=np.float32)

    next_obs, next_state, rewards, done, info = env.step(actions)

    assert obs.shape == (env.n_agents, env.local_obs_dim)
    assert state.shape == (env.global_state_dim,)
    assert next_obs.shape == obs.shape
    assert next_state.shape == state.shape
    assert rewards.shape == (env.n_agents,)
    assert np.isfinite(rewards).all()
    assert isinstance(done, bool)
    assert info["policy_mode"] == "learned"


def test_ablation_config_affects_env_and_cache_lookup():
    single = cfg.resolve_ablation("single_timescale")
    env = MultiUAVMECEnv(
        seed=2,
        domain_cfg=small_domain(),
        ablation_config=single,
    )
    _, _ = env.reset()
    actions = np.zeros((env.n_agents, env.agent_action_dim), dtype=np.float32)
    _, _, _, _, info = env.step(actions)
    assert env.cache_timescale_k_c == 1
    assert info["macro_interval_len"] == 1
    assert info["is_macro_step"]

    no_coop = cfg.resolve_ablation("no_coop_cache")
    env = MultiUAVMECEnv(
        seed=3,
        domain_cfg=small_domain(),
        ablation_config=no_coop,
    )
    env.cache_manager.uav_caches = [[], [0], []]
    tier, delay, partner = env.cache_manager.lookup(0, 0)
    assert not env.cache_manager.use_coop_cache
    assert tier == 3
    assert partner is None


def test_no_diffusion_ablation_uses_gaussian_actor():
    previous_mode = cfg.ABLATION_MODE
    try:
        cfg.apply_ablation("no_diffusion")
        env = MultiUAVMECEnv(
            seed=4,
            domain_cfg=small_domain(),
            ablation_config=cfg.current_ablation_config(),
        )
        agent = make_agent(
            "DMJO",
            env.local_obs_dim,
            env.global_state_dim,
            env.agent_action_dim,
            env.n_agents,
            device="cpu",
        )
        assert isinstance(agent.actor, GaussianOnlyActor)
    finally:
        cfg.apply_ablation(previous_mode)


def test_noma_serves_at_most_two_devices_per_uav():
    env = MultiUAVMECEnv(seed=5, domain_cfg=small_domain(num_users=24, num_uavs=3))
    env.reset()
    actions = np.zeros((env.n_agents, env.agent_action_dim), dtype=np.float32)
    actions[:, 3] = 1.0
    _, _, _, _, info = env.step(actions)

    for selected in info["scheduled_dev_ids_by_agent"].values():
        assert len(selected) <= 2


def test_schedule_hint_changes_primary_selection():
    env = MultiUAVMECEnv(seed=6, domain_cfg=small_domain(num_users=6, num_uavs=3))
    env.reset()
    devices = env.devices[:4]
    gains = np.array([0.2, 0.5, 0.8, 0.4])
    low_hint = np.array([0, 0, 0, 1, -1.0], dtype=np.float32)
    high_hint = np.array([0, 0, 0, 1, 1.0], dtype=np.float32)

    low_devs, _, low_ids = env._select_noma_devices(devices, gains, low_hint, env.uavs[0])
    high_devs, _, high_ids = env._select_noma_devices(devices, gains, high_hint, env.uavs[0])

    assert low_devs[0].id == devices[0].id
    assert high_devs[0].id == devices[-1].id
    assert low_ids != high_ids


def test_local_execution_policy_has_no_cache_or_uav_offload():
    env = MultiUAVMECEnv(
        seed=7,
        domain_cfg=small_domain(),
        policy_mode="local_execution",
    )
    env.reset()
    actions = np.zeros((env.n_agents, env.agent_action_dim), dtype=np.float32)
    _, _, _, _, info = env.step(actions)

    assert info["policy_mode"] == "local_execution"
    assert info["uav_compute"] == 0
    assert info["cache_local_hits"] == 0
    assert info["cache_coop_hits"] == 0
    assert info["cache_bs_fetches"] == 0


def test_greedy_policy_uses_nearest_uav_clusters():
    env = MultiUAVMECEnv(
        seed=8,
        domain_cfg=small_domain(num_users=3, num_uavs=3),
        policy_mode="greedy_offloading",
    )
    env.reset()
    for i, pos in enumerate([(0, 0), (100, 0), (0, 100)]):
        env.uavs[i].position[:2] = np.array(pos, dtype=float)
    for i, pos in enumerate([(3, 0, 0), (97, 0, 0), (0, 98, 0)]):
        env.devices[i].position[:] = np.array(pos, dtype=float)

    env._assign_clusters()

    assert [d.cluster_id for d in env.devices[:3]] == [0, 1, 2]
