# MAPPO Project Tracker

AI agents should read `AGENTS.md` and `docs/methodology/AI_AGENT_CONTEXT.md` before using this tracker.

---

## 1. Current Direction & Status

This codebase is **MAPPO-first**: a flexible multi-UAV MEC-IoT framework with plain MAPPO, cooperative caching, NOMA scheduling, jamming, wind, and comparison baselines. The earlier `uav_trajectory_rl` project remains a validated reference for testing and physical-model review discipline, not a source of strict algorithmic constraints for this repository.

The project is not diffusion-based. Diffusion-related classes remain only as legacy optional experiment code and are not part of the final evaluated method.

---

## 2. Locked Runtime Interfaces

- Environment entrypoint: `MultiUAVMECEnv(..., policy_mode="learned", ablation_config=None)`.
- Supported policy modes: `learned`, `greedy_offloading`, `local_execution`.
- Per-agent action shape remains `(n_agents, 5)` with `[dx, dy, dh, offload_bias, schedule_hint]`.
- `train.py --method ... --ablation ...` remains the public training interface.
- Existing method names remain accepted: `MAPPO`, `DMJO`, `MADDPG`, `MATD3`, `GreedyOffloading`, `LocalExecution`.
- `MAPPO` is the primary method and default.
- `DMJO` is a backward-compatible alias for the MAPPO implementation.

---

## 3. Design Decisions

- Runtime ablations are resolved in `config.apply_ablation()` and passed into environments so modules do not rely on stale import-time copies.
- MAPPO uses PPO rollout buffers that train only on filled rollout steps; partial final rollouts no longer include zero-padded transitions.
- Learned methods use action-controlled scheduling: `offload_bias < 0` tries local compute first, otherwise the task goes to UAV/cache handling.
- NOMA service is capped at two devices per UAV per slot to match the project description.
- `GreedyOffloading` uses nearest-UAV clustering and fixed simple trajectories, but does not make cache-aware learned scheduling decisions.
- `LocalExecution` bypasses UAV/cache offloading entirely.
- `no_diffusion` remains a CLI-compatible ablation label, but it is not a scientific ablation for the final project because the full MAPPO method is already non-diffusion.

---

## 4. Verification Scope & Completed Milestones

- **Unit, Integration & Smoke Tests:** 10/10 automated tests pass in pytest (`tests/unit/`, `tests/integration/`, `tests/smoke/`).
- **5,000,000-Step Training Completed:**
  - **MAPPO (Proposed):** Converged reward `$-23,275.82$`, average latency `181.2` ms.
  - **GreedyOffloading (Baseline 1):** Converged reward `$-42,840.95$`, average latency `332.1` ms.
  - **LocalExecution (Baseline 2):** Converged reward `$-8,287.92$` (zero offload, local only).
- **Publication Figures:** All 56 IEEE publication figures (PDF + PNG) generated in `results/plots/`.
- **Checkpoints & Telemetry:** 39 checkpoints saved in `results/checkpoints/`, 51 trajectory files in `results/trajectories/`, full telemetry in `results/logs/`.
- **Conference Paper:** Section V (Simulation Results) fully populated with comparison tables and 15 figures in `docs/reports/paper/paper.tex`.
