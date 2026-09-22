# MAPPO Project Tracker

## Current Direction

This codebase is MAPPO-first: a flexible multi-UAV MEC-IoT framework with
plain MAPPO, cooperative caching, NOMA scheduling, jamming, wind, and comparison
baselines. The earlier `uav_trajectory_rl` project remains a validated
reference for testing and physical-model review discipline, not a source of
strict algorithmic constraints for this repository.

The project is not diffusion-based. Diffusion-related classes remain only as
legacy optional experiment code and should not be claimed as part of the final
method.

## Locked Runtime Interfaces

- Environment entrypoint: `MultiUAVMECEnv(..., policy_mode="learned", ablation_config=None)`.
- Supported policy modes: `learned`, `greedy_offloading`, `local_execution`.
- Per-agent action shape remains `(n_agents, 5)` with `[dx, dy, dh, offload_bias, schedule_hint]`.
- `train.py --method ... --ablation ...` remains the public training interface.
- Existing method names remain accepted: `MAPPO`, `DMJO`, `MADDPG`, `MATD3`, `GreedyOffloading`, `LocalExecution`.
- `MAPPO` is the main method and default.
- `DMJO` is a backward-compatible alias for the MAPPO implementation.

## Design Decisions

- Runtime ablations are resolved in `config.apply_ablation()` and passed into environments so modules do not rely on stale import-time copies.
- MAPPO uses PPO rollout buffers that train only on filled rollout steps; partial final rollouts no longer include zero-padded transitions.
- Learned methods use action-controlled scheduling: `offload_bias < 0` tries local compute first, otherwise the task goes to UAV/cache handling.
- NOMA service is capped at two devices per UAV per slot to match the project description.
- `GreedyOffloading` uses nearest-UAV clustering and fixed simple trajectories, but does not make cache-aware learned scheduling decisions.
- `LocalExecution` bypasses UAV/cache offloading entirely.
- `no_diffusion` remains a CLI-compatible ablation label, but it is not a scientific ablation for the final project because the full MAPPO method is already non-diffusion.

## Verification Scope

- Unit tests cover environment shape/finite rewards, runtime ablation effects, NOMA cap, schedule hint selection, local-only behavior, greedy nearest association, partial rollout handling, and one-step smoke execution for all six methods.
- Existing trained checkpoints/results should be considered stale after these behavior changes.
