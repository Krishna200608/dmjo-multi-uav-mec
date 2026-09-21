# DMJO Implementation Tracker

## Current Direction

This codebase is DMJO-first: a flexible multi-UAV MEC-IoT framework with diffusion-enhanced MAPPO, cooperative caching, NOMA scheduling, jamming, wind, and comparison baselines. The earlier `uav_trajectory_rl` project remains a validated reference for testing and physical-model review discipline, not a source of strict algorithmic constraints for this repository.

## Locked Runtime Interfaces

- Environment entrypoint: `MultiUAVMECEnv(..., policy_mode="learned", ablation_config=None)`.
- Supported policy modes: `learned`, `greedy_offloading`, `local_execution`.
- Per-agent action shape remains `(n_agents, 5)` with `[dx, dy, dh, offload_bias, schedule_hint]`.
- `train.py --method ... --ablation ...` remains the public training interface.
- Existing method names remain unchanged: `DMJO`, `MAPPO`, `MADDPG`, `MATD3`, `GreedyOffloading`, `LocalExecution`.

## Design Decisions

- Runtime ablations are resolved in `config.apply_ablation()` and passed into environments so modules do not rely on stale import-time copies.
- DMJO and MAPPO use PPO rollout buffers that train only on filled rollout steps; partial final rollouts no longer include zero-padded transitions.
- Learned methods use action-controlled scheduling: `offload_bias < 0` tries local compute first, otherwise the task goes to UAV/cache handling.
- NOMA service is capped at two devices per UAV per slot to match the project description.
- `GreedyOffloading` uses nearest-UAV clustering and fixed simple trajectories, but does not make cache-aware learned scheduling decisions.
- `LocalExecution` bypasses UAV/cache offloading entirely.

## Verification Scope

- Unit tests cover environment shape/finite rewards, runtime ablation effects, NOMA cap, schedule hint selection, local-only behavior, greedy nearest association, partial rollout handling, and one-step smoke execution for all six methods.
- Existing trained checkpoints/results should be considered stale after these behavior changes.
