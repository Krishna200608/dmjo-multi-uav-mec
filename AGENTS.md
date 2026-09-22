# AI Agent Instructions

This repository is the final project codebase for MAPPO-based multi-UAV MEC.
Read this file before making code, documentation, experiment, or result changes.

## Project Truth

- The claimed method is plain MAPPO, not diffusion.
- `MAPPO` is the main method and default CLI method.
- `DMJO` is only a backward-compatible alias for the same MAPPO implementation.
- `--ablation no_diffusion` is only a compatibility label. It is not a final scientific ablation because the full method is already non-diffusion.
- `src/diffusion.py` is legacy optional experiment code. Do not describe it as part of the final method.
- Fresh result production should use `python train.py --method MAPPO ...`.
- Old diffusion-labelled checkpoints, plots, and result folders are stale.

## Files To Read First

1. `README.md` - human-facing overview, install, train, evaluate.
2. `docs/AI_AGENT_CONTEXT.md` - full technical handoff for AI agents.
3. `docs/MAPPO_Project_Tracker.md` - locked project direction and assumptions.
4. `docs/RUN_ON_CAMPUS_MACHINE.md` - exact run commands for GPU/campus machine.
5. `config.py` - constants, ablations, runtime flags.
6. `src/env.py` - environment dynamics, action semantics, policy modes.
7. `src/mappo_agent.py` - final MAPPO policy implementation.
8. `train.py` - public CLI entrypoint.

## Public Interfaces To Preserve

- Environment constructor:

```python
MultiUAVMECEnv(..., policy_mode="learned", ablation_config=None)
```

- Per-agent action shape:

```text
(n_agents, 5)
```

- Per-agent action meaning:

```text
[dx, dy, dh, offload_bias, schedule_hint]
```

- CLI entrypoint:

```bash
python train.py --method MAPPO --ablation full ...
```

- Accepted method names:

```text
MAPPO, DMJO, MADDPG, MATD3, GreedyOffloading, LocalExecution
```

- Accepted ablation names:

```text
full, single_timescale, no_diffusion, no_mappo_traj, no_coop_cache, minimal
```

## Behavioral Rules

- Keep NOMA service capped at at most two IoT devices per active UAV per slot.
- Keep `schedule_hint` deterministic for primary eligible device selection.
- Keep `offload_bias < 0` as local-first and `offload_bias >= 0` as UAV/cache-first.
- Keep `LocalExecution` strictly local: no UAV compute, no cache lookup, no BS fetch.
- Keep `GreedyOffloading` as nearest-UAV association with fixed simple trajectory and no learned scheduling.
- Keep rollout updates limited to filled buffer steps. Do not train PPO on zero-padded partial rollouts.
- Keep runtime ablations resolved through `config.apply_ablation()` and passed into environments. Avoid import-time copies of mutable config flags.

## Testing And Verification

Local syntax check:

```bash
python -m compileall config.py src train.py test_custom.py
```

Unit tests:

```bash
python -m pytest tests -q
```

Tiny smoke:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

Expected tests:

```text
10 passed
```

Expected smoke startup:

```text
Method      : MAPPO
Agent: MAPPO
diffusion=False
```

## Git And Generated Files

- `results/`, `.venv/`, caches, and pyc files are ignored by Git.
- Do not commit generated checkpoints, plots, logs, videos, cache folders, or virtualenvs.
- If changing behavior, update tests and the relevant docs in the same change.
- If producing result runs, keep them in `results/` and copy them separately from Git.

## Common Pitfalls

- Do not reintroduce diffusion as the claimed method.
- Do not treat `DMJO` and `MAPPO` as different learned algorithms unless the project direction explicitly changes again.
- Do not use `--checkpoint` as a training resume feature. In `train.py`, checkpoint loading is evaluation-only.
- Do not train `uav_trajectory_rl` for final results; it is only an external reference project.
- Do not rely on old checkpoint folders when comparing results after behavior changes.
