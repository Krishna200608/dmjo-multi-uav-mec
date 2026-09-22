# MAPPO Multi-UAV MEC

MAPPO-based joint optimization for UAV-assisted Mobile Edge Computing (MEC).

This repository is the final project codebase. The implemented and claimed
learning approach is a simple Multi-Agent Proximal Policy Optimization (MAPPO)
method with a centralised critic and decentralised UAV actors. It is not a
diffusion-based method.

The older `uav_trajectory_rl` folder is only a reference for testing discipline,
physics sanity checks, and documentation style.

## What This Project Optimizes

The environment models a jammer-aware multi-UAV MEC-IoT network with:

- MAPPO trajectory control for multiple UAVs.
- Task offloading decisions between local execution and MEC handling.
- Cooperative UAV service caching.
- NOMA uplink scheduling with at most two IoT devices served per UAV per slot.
- Heterogeneous UAV profiles.
- IoT mobility, wind effects, and jammer interference.
- Baseline methods for comparison.

The objective is to reduce latency and UAV energy cost:

```text
cost(t) = alpha * latency(t) + beta * UAV_energy(t)
```

Default weights:

```text
alpha = 0.6
beta  = 0.4
```

## Important Naming Note

Some file names and command-line options still contain `DMJO` because the code
was previously shaped around a diffusion-based draft. After the project update:

- `MAPPO` is the main method and the default.
- `DMJO` is kept only as a backward-compatible CLI alias.
- `--ablation no_diffusion` is kept only for compatibility; the full method is
  already non-diffusion.
- The file `src/diffusion.py` remains only as legacy optional experiment code.

Fresh results should be generated with `--method MAPPO`.

For AI coding agents or future maintainers, read `AGENTS.md` first, then
`docs/AI_AGENT_CONTEXT.md`.

## Repository Structure

```text
dmjo-multi-uav-mec/
|-- AGENTS.md
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
`-- src/
    |-- env.py
    |-- mappo_agent.py
    |-- caching.py
    |-- channel_model.py
    |-- buffer.py
    |-- metrics.py
    |-- logger.py
    |-- agent_factory.py
    |-- diffusion.py          # legacy optional experiment code
    `-- baselines/
        |-- mappo_baseline.py # legacy wrapper
        |-- maddpg_agent.py
        |-- matd3_agent.py
        |-- greedy_agent.py
        `-- local_agent.py
```

## Action Space

Each UAV agent emits a 5D continuous action in `[-1, 1]`:

```text
[dx, dy, dh, offload_bias, schedule_hint]
```

- `dx`, `dy`, `dh`: UAV trajectory movement.
- `offload_bias < 0`: local-first task handling.
- `offload_bias >= 0`: UAV/cache-first MEC handling.
- `schedule_hint`: selects the primary eligible IoT device for NOMA service.

NOMA service is capped at two IoT devices per UAV per slot.

## Policy Modes

The environment supports explicit policy modes:

```text
learned
greedy_offloading
local_execution
```

Method mapping:

| Method | Policy mode | Role |
|---|---|---|
| `MAPPO` | `learned` | Main method |
| `DMJO` | `learned` | Legacy alias for MAPPO |
| `MADDPG` | `learned` | Off-policy baseline |
| `MATD3` | `learned` | Off-policy baseline |
| `GreedyOffloading` | `greedy_offloading` | Nearest-UAV rule baseline |
| `LocalExecution` | `local_execution` | All tasks local baseline |

## Installation

Python 3.10 or newer is recommended. Python 3.11 was used locally.

```bash
git clone git@github.com:Krishna200608/dmjo-multi-uav-mec.git
cd dmjo-multi-uav-mec
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
cd "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec"
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Quick Verification

Run tests:

```bash
python -m pytest tests -q
```

Expected:

```text
10 passed
```

Run a tiny smoke test:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

With CUDA:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cuda --no-training-video --smoke-test
```

## Training

Main MAPPO run:

```bash
python -u train.py --method MAPPO --ablation full --device cuda --no-training-video
```

CPU run:

```bash
python -u train.py --method MAPPO --ablation full --device cpu --no-training-video
```

Default total training budget:

```text
TOTAL_TIMESTEPS = 5,000,000
```

Output paths:

```text
results/checkpoints/MAPPO/full/
results/logs/MAPPO/full/
results/trajectories/
results/videos/
```

Important checkpoints:

```text
best_model.pt
final_model.pt
model_step*.pt
```

## Baseline Runs

```bash
python -u train.py --method MAPPO            --ablation full --device cuda --no-training-video
python -u train.py --method MADDPG           --ablation full --device cuda --no-training-video
python -u train.py --method MATD3            --ablation full --device cuda --no-training-video
python -u train.py --method GreedyOffloading --ablation full --device cuda --no-training-video
python -u train.py --method LocalExecution   --ablation full --device cuda --no-training-video
```

`DMJO` can still be run, but it is only an alias for the MAPPO policy path:

```bash
python -u train.py --method DMJO --ablation full --device cuda --no-training-video
```

Use `MAPPO` in reports and final result tables.

## Ablations

```bash
python -u train.py --method MAPPO --ablation full             --device cuda --no-training-video
python -u train.py --method MAPPO --ablation single_timescale --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_mappo_traj    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_coop_cache    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation minimal          --device cuda --no-training-video
```

Compatibility-only ablation:

```bash
python -u train.py --method MAPPO --ablation no_diffusion --device cuda --no-training-video
```

`no_diffusion` should not be treated as a scientific ablation in the final
report because the main method is already non-diffusion.

## Evaluation

```bash
python train.py \
  --method MAPPO \
  --ablation full \
  --eval \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --device cuda
```

Custom environment evaluation:

```bash
python test_custom.py \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --num-iot 120 \
  --num-uavs 6 \
  --num-jammers 2 \
  --episodes 20 \
  --device cuda
```

Important: `--checkpoint` in `train.py` is for evaluation mode only. Training
does not automatically resume optimizer/model state from a checkpoint.

## Figures

After training/evaluation data exists:

```bash
python plot_ieee.py
```

Expected output:

```text
results/plots/
```

## Generated Files

The complete `results/` folder is ignored by Git. Bring trained outputs back
from the campus machine manually:

```text
results/checkpoints/
results/logs/
results/plots/
results/test_results/
results/trajectories/
run_*.log
```

## Current Verification

Local verification after the MAPPO-first correction should include:

```bash
python -m pytest tests -q
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

Old checkpoints and plots from diffusion-labelled runs should be considered
stale for the final project.
