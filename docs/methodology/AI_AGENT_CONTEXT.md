# AI Agent Project Context

This file is a technical handoff for any AI coding agent that receives this
repository. It explains the project identity, current implementation, public
interfaces, run commands, known caveats, and the most important files.

## One-Sentence Summary

This repository implements a MAPPO-based multi-UAV MEC optimizer for trajectory,
task offloading, cooperative caching, and NOMA scheduling in a jammer-aware IoT
network.

## Current Project Identity

- Repository folder: `dmjo-multi-uav-mec`
- GitHub remote: `git@github.com:Krishna200608/dmjo-multi-uav-mec.git`
- Final method: plain MAPPO with centralised critic and decentralised UAV actors
- Not final method: diffusion, diffusion-MAPPO, or diffusion-enhanced DRL
- Main CLI method: `MAPPO`
- Legacy CLI alias: `DMJO`

The project originally had diffusion/DMJO wording. That direction was corrected.
Some names remain for compatibility, but final claims, docs, training commands,
and result tables should use `MAPPO`.

## Historical Context

There is another folder outside this repo named `uav_trajectory_rl`. It was used
as a reference for testing discipline, physical sanity checks, and documentation
style. It is not the final algorithm and should not be trained for final results.

The earlier DMJO/diffusion draft left behind:

- `src/diffusion.py`
- `DMJO` as an accepted method name
- `no_diffusion` as an accepted ablation name

These are compatibility artifacts. They should not be turned back into final
project claims unless the user explicitly changes the project direction again.

## Repository Map

```text
dmjo-multi-uav-mec/
|-- AGENTS.md
|-- README.md
|-- config.py
|-- train.py
|-- test_custom.py
|-- plot_ieee.py
|-- requirements.txt
|-- docs/
|   |-- AI_AGENT_CONTEXT.md
|   |-- MAPPO_Project_Tracker.md
|   `-- RUN_ON_CAMPUS_MACHINE.md
|-- tests/
|   |-- test_buffer.py
|   |-- test_dmjo_env.py
|   `-- test_method_smoke.py
`-- src/
    |-- __init__.py
    |-- agent_factory.py
    |-- buffer.py
    |-- caching.py
    |-- channel_model.py
    |-- diffusion.py
    |-- env.py
    |-- logger.py
    |-- mappo_agent.py
    |-- metrics.py
    `-- baselines/
        |-- greedy_agent.py
        |-- local_agent.py
        |-- maddpg_agent.py
        |-- mappo_baseline.py
        `-- matd3_agent.py
```

## Core Runtime Flow

The normal execution path is:

```text
train.py
  -> config.apply_ablation(args.ablation)
  -> MultiUAVMECEnv(policy_mode=..., ablation_config=...)
  -> make_agent(method=...)
  -> rollout collection
  -> RolloutBuffer.compute_gae()
  -> MAPPOAgent.update()
  -> checkpoints/logs/plots under results/
```

## Main Files And Responsibilities

### `config.py`

Holds all environment constants, MAPPO hyperparameters, training intervals, and
runtime ablation helpers.

Important functions:

- `resolve_ablation(mode)`
- `apply_ablation(mode)`
- `current_ablation_config()`

Important truth:

- `USE_DIFFUSION = False`
- `full` has `"use_diffusion": False`
- `no_diffusion` exists only as compatibility

### `train.py`

Main CLI entrypoint for training/evaluation.

Default:

```bash
python train.py --method MAPPO --ablation full
```

Important flags:

- `--method`
- `--ablation`
- `--total-steps`
- `--device`
- `--eval`
- `--checkpoint`
- `--no-training-video`
- `--smoke-test`

Important caveat:

`--checkpoint` is evaluation-only. Training does not resume optimizer/model
state from a checkpoint.

### `src/env.py`

The multi-UAV MEC environment.

Constructor:

```python
MultiUAVMECEnv(..., policy_mode="learned", ablation_config=None)
```

Policy modes:

- `learned`
- `greedy_offloading`
- `local_execution`

Action shape:

```text
(n_agents, 5)
```

Action meaning:

```text
[dx, dy, dh, offload_bias, schedule_hint]
```

Semantics:

- `dx`, `dy`, `dh`: UAV trajectory movement
- `offload_bias < 0`: local-first handling
- `offload_bias >= 0`: UAV/cache-first handling
- `schedule_hint`: primary eligible IoT device selection
- NOMA service is capped at two devices per active UAV per slot

### `src/mappo_agent.py`

The final learned method implementation.

Uses:

- Gaussian actor (`GaussianOnlyActor`)
- centralised critic
- PPO clipped objective
- GAE
- entropy bonus

Does not use:

- diffusion sampling
- diffusion loss
- diffusion blend annealing

### `src/agent_factory.py`

Creates all agents from method names.

Accepted methods:

```text
MAPPO, DMJO, MADDPG, MATD3, GreedyOffloading, LocalExecution
```

Important:

- `MAPPO` returns `MAPPOAgent`
- `DMJO` also returns `MAPPOAgent` as a legacy alias
- `MADDPG` and `MATD3` are off-policy baselines
- `GreedyOffloading` and `LocalExecution` are rule-based baselines

### `src/buffer.py`

PPO rollout buffer. It must train only on filled rollout steps, especially for
partial final rollouts. Do not reintroduce updates over zero padding.

### `src/caching.py`

Three-tier service cache:

1. Local UAV cache
2. Cooperative A2A peer fetch
3. Base station backhaul

`no_coop_cache` disables tier-2 cooperative lookup.

### `src/channel_model.py`

Wireless channel and NOMA communication helpers.

### `src/logger.py`

Writes training metrics, trajectory snapshots, cache stats, episode summaries,
and parameter sweep data.

### `plot_ieee.py`

Generates result plots from files under `results/`. It should not need to train
the agent.

### `test_custom.py`

Evaluation script for custom environment configurations.

## Method And Policy Mode Mapping

| Method | Agent class | Policy mode | Role |
|---|---|---|---|
| `MAPPO` | `MAPPOAgent` | `learned` | Main method |
| `DMJO` | `MAPPOAgent` | `learned` | Legacy alias |
| `MADDPG` | `MADDPGAgent` | `learned` | Off-policy baseline |
| `MATD3` | `MATD3Agent` | `learned` | Off-policy baseline |
| `GreedyOffloading` | `GreedyOffloadingAgent` | `greedy_offloading` | Rule baseline |
| `LocalExecution` | `LocalExecutionAgent` | `local_execution` | Rule baseline |

## Ablation Semantics

| Ablation | Meaning |
|---|---|
| `full` | Main MAPPO-MEC setup |
| `single_timescale` | `K_C = 1`, cache updated every slot |
| `no_diffusion` | Compatibility alias only; main method is already non-diffusion |
| `no_mappo_traj` | Fixed circular UAV orbits |
| `no_coop_cache` | Local cache + BS only; cooperative A2A cache disabled |
| `minimal` | No cooperative cache, plain MAPPO actor |

For final reporting, prefer:

```text
full, single_timescale, no_mappo_traj, no_coop_cache, minimal
```

Avoid presenting `no_diffusion` as a meaningful final ablation.

## Output Structure

Generated files go under `results/`, which is ignored by Git.

Common paths:

```text
results/checkpoints/<method>/<ablation>/
results/logs/<method>/<ablation>/
results/logs/training_metrics.jsonl
results/trajectories/
results/videos/
results/plots/
results/test_results/
```

Important checkpoint files:

```text
best_model.pt
final_model.pt
model_step*.pt
```

Do not commit `results/`.

## Verification Commands

Syntax:

```bash
python -m compileall config.py src train.py test_custom.py
```

Tests:

```bash
python -m pytest tests -q
```

Expected:

```text
10 passed
```

MAPPO smoke:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

Expected startup should include:

```text
Method      : MAPPO
Agent: MAPPO
diffusion=False
```

Legacy alias smoke, if needed:

```bash
python train.py --method DMJO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

It should still print `Agent: MAPPO` and `diffusion=False`.

## Campus/GPU Result Commands

Main final run:

```bash
python -u train.py --method MAPPO --ablation full --device cuda --no-training-video
```

Baselines:

```bash
python -u train.py --method MADDPG           --ablation full --device cuda --no-training-video
python -u train.py --method MATD3            --ablation full --device cuda --no-training-video
python -u train.py --method GreedyOffloading --ablation full --device cuda --no-training-video
python -u train.py --method LocalExecution   --ablation full --device cuda --no-training-video
```

Ablations:

```bash
python -u train.py --method MAPPO --ablation single_timescale --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_mappo_traj    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_coop_cache    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation minimal          --device cuda --no-training-video
```

See `docs/RUN_ON_CAMPUS_MACHINE.md` for full machine setup, proxy, monitoring,
evaluation, plotting, and result-copy instructions.

## Development Rules For Future AI Agents

- Keep claims truthful to code behavior.
- Do not make the project diffusion-based unless the user explicitly requests a new project direction.
- If behavior changes, update docs and tests together.
- Prefer focused patches over broad refactors.
- Preserve CLI compatibility unless asked otherwise.
- Preserve output directory layout unless asked otherwise.
- Keep generated files out of Git.
- Run at least `pytest tests -q` after behavior changes when dependencies are available.

## Known Caveats

- Training resume from checkpoint is not implemented.
- `src/diffusion.py` is legacy code and may confuse readers; keep docs clear.
- Some test names still contain `dmjo` because they were created before the MAPPO-first correction.
- Local laptop may not have GPU. Campus machine or supervisor CPU/GPU machine is intended for final result production.
- `.venv/` may exist locally but is ignored and should not be pushed.

## Last Verified State

After the MAPPO-first correction, local verification passed with:

```text
compileall passed
pytest: 10 passed
MAPPO smoke: passed with diffusion=False
```
