# MAPPO Multi-UAV MEC: Joint Trajectory, Offloading, Cooperative Caching, and NOMA Optimization

Multi-Agent Proximal Policy Optimization (MAPPO) for UAV-assisted Mobile Edge Computing (MEC) in Jammer-Aware IoT Networks.

This repository hosts the official implementation of our paper on **MAPPO-based Multi-UAV Mobile Edge Computing**. The learning architecture is formulated around **Multi-Agent Proximal Policy Optimization (MAPPO)** under the Centralised Training with Decentralised Execution (CTDE) paradigm, featuring a centralised critic and decentralised UAV actors.

---

## Academic Context & Base Paper

This research builds upon and substantially expands the theoretical and physical foundation established in:

> **Base Paper:**  
> M. Li, M. Dong, H. Wang, and H. Wang, *"3-D Trajectory Design Based on Deep Reinforcement Learning for UAV-Assisted Communication Networks"*, **IEEE Transactions on Network Science and Engineering**, vol. 13, no. 1, pp. 248–261, 2026.  
> *Document location: `docs/Base Paper/3-D_Trajectory_Design_Based_on_Deep_Reinforcement_Learning_for_UAV-Assisted_Communication_Networks.pdf`*

### Research Evolution & Architectural Extensions

While the base paper investigated 3-D trajectory design for a **single UAV** acting as an aerial communication relay for moving ground users via single-agent RL (PKTD3-TD), our paper advances this framework into a comprehensive **Multi-UAV Mobile Edge Computing (MEC)** and cooperative networking architecture:

| System Dimension | Base Paper (Li et al., *IEEE TNSE* 2026) | Our Work (Final Multi-UAV MEC Architecture) |
|---|---|---|
| **Fleet Topology** | Single UAV relay / aerial base station | **Multi-UAV cooperative fleet** with heterogeneous compute & flight profiles |
| **Learning Paradigm** | Single-Agent TD3 (PKTD3-TD with prior knowledge) | **Multi-Agent PPO (MAPPO)** with Centralised Critic & Decentralised Actors (CTDE) |
| **Decision Variables** | 3-D Trajectory displacement only ($\Delta x, \Delta y, \Delta h$) | **Joint 5-D Action**: 3-D Trajectory, Offloading Bias, and NOMA Schedule Hint |
| **Computation Layer** | None (pure communication / data relaying) | **2-Tier MEC**: Local IoT execution vs. UAV edge server / BS cloud computing |
| **Service Caching** | None | **3-Tier Cooperative Caching**: Local UAV $\leftrightarrow$ A2A Peer Fetch $\leftrightarrow$ Macro BS Backhaul |
| **Multiple Access** | Orthogonal Multiple Access (OMA / TDMA) | **Power-domain Uplink NOMA** with Successive Interference Cancellation (SIC) |
| **Hostile Dynamics** | Random user mobility (Gauss-Markov) | Random user mobility + **Active RF jammers** + **Wind vector turbulence** |
| **System Objective** | Maximize network throughput; minimize propulsion energy | **Jointly minimize end-to-end task completion latency and UAV energy consumption** |

---

## What This Project Optimizes

The environment models a jammer-aware multi-UAV MEC-IoT network featuring:

- **MAPPO 3-D Trajectory Control**: Autonomous navigation of multiple heterogeneous UAVs in continuous 3-D space with collision avoidance and flight constraints.
- **Adaptive Task Offloading**: Dynamic allocation between low-power local IoT computation and high-speed MEC edge offloading.
- **3-Tier Cooperative Caching**: Service resolution across local UAV cache, Air-to-Air (A2A) peer cooperative cache sharing, and Base Station (BS) backhaul retrieval.
- **Uplink NOMA Scheduling**: Non-Orthogonal Multiple Access with SIC serving at most two IoT devices per active UAV per time slot.
- **Realistic Physical Dynamics**: Rician small-scale fading, probabilistic LoS/NLoS channel modeling, wind drift, and active malicious jamming interference.
- **Comprehensive Baseline Suite**: Rigorous comparison against MADDPG, MATD3, Greedy Offloading, and Local Execution.

### Optimization Objective

The primary objective is to minimize total system cost, defined as the weighted trade-off between task completion latency and UAV energy expenditure:

$$\text{Cost}(t) = \alpha \cdot \text{Latency}(t) + \beta \cdot E_{\text{UAV}}(t)$$

where:
- $\text{Latency}(t)$ is the end-to-end execution delay across all generated tasks in slot $t$ (incorporating transmission, queuing, caching fetch, and compute delays).
- $E_{\text{UAV}}(t)$ is the sum of UAV aerodynamic propulsion energy (flight dynamics) and edge CPU computation energy.
- $\alpha = 0.6$ and $\beta = 0.4$ are the default weighting coefficients balancing QoS latency constraints and aerial energy budgets.

---

## Important Naming Note

Some file names and command-line options still contain `DMJO` because the code was previously shaped around a diffusion-based draft. After the project update:

- `MAPPO` is the main method and the default CLI method.
- `DMJO` is kept strictly as a backward-compatible CLI alias.
- `--ablation no_diffusion` is kept only for compatibility; the full method is already non-diffusion.
- The file `src/diffusion.py` remains only as legacy optional experiment code.

Fresh results should always be generated with `--method MAPPO`.

For AI coding agents or future maintainers, read [AGENTS.md](file:///d:/Lab/Data%20Management%20in%20Mobile%20and%20Sensor%20Networks/dmjo-multi-uav-mec/AGENTS.md) first, followed by [docs/AI_AGENT_CONTEXT.md](file:///d:/Lab/Data%20Management%20in%20Mobile%20and%20Sensor%20Networks/dmjo-multi-uav-mec/docs/AI_AGENT_CONTEXT.md).

---

## Repository Structure

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
|   |-- RUN_ON_CAMPUS_MACHINE.md
|   `-- Base Paper/
|       `-- 3-D_Trajectory_Design_Based_on_Deep_Reinforcement_Learning_for_UAV-Assisted_Communication_Networks.pdf
|-- tests/
|   |-- test_buffer.py
|   |-- test_dmjo_env.py
|   `-- test_method_smoke.py
`-- src/
    |-- __init__.py
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

---

## Action Space

Each UAV agent emits a 5-D continuous action vector $\mathbf{a}_i \in [-1, 1]^5$:

```text
[dx, dy, dh, offload_bias, schedule_hint]
```

- `dx`, `dy`, `dh`: 3-D UAV displacement in horizontal and vertical axes, scaled by maximum flight speeds.
- `offload_bias < 0`: Local-first task handling (IoT device attempts local execution).
- `offload_bias >= 0`: UAV/cache-first MEC offloading handling.
- `schedule_hint`: Selects the primary eligible IoT device for NOMA uplink transmission.

> **Note**: NOMA uplink service is strictly capped at at most two IoT devices per active UAV per time slot.

---

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
| `MAPPO` | `learned` | Main proposed method |
| `DMJO` | `learned` | Backward-compatible alias for MAPPO |
| `MADDPG` | `learned` | Multi-agent off-policy baseline |
| `MATD3` | `learned` | Multi-agent off-policy baseline |
| `GreedyOffloading` | `greedy_offloading` | Nearest-UAV heuristic baseline |
| `LocalExecution` | `local_execution` | Strictly local execution baseline |

---

## Installation

Python 3.10 or newer is recommended. Python 3.11 is verified locally.

### Linux / macOS

```bash
git clone git@github.com:Krishna200608/dmjo-multi-uav-mec.git
cd dmjo-multi-uav-mec
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
cd "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec"
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Quick Verification

Run unit test suite:

```bash
python -m pytest tests -q
```

Expected output:
```text
10 passed
```

Run a tiny CPU smoke test:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

Run with CUDA:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cuda --no-training-video --smoke-test
```

---

## Training

### Main MAPPO Run (GPU)

```bash
python -u train.py --method MAPPO --ablation full --device cuda --no-training-video
```

### CPU Run

```bash
python -u train.py --method MAPPO --ablation full --device cpu --no-training-video
```

Default total training budget:
```text
TOTAL_TIMESTEPS = 5,000,000
```

### Output Directories

Generated artifacts are stored in `results/`:

```text
results/checkpoints/MAPPO/full/
results/logs/MAPPO/full/
results/trajectories/
results/videos/
```

Key checkpoint weights:
```text
best_model.pt
final_model.pt
model_step*.pt
```

---

## Baseline Runs

```bash
python -u train.py --method MAPPO            --ablation full --device cuda --no-training-video
python -u train.py --method MADDPG           --ablation full --device cuda --no-training-video
python -u train.py --method MATD3            --ablation full --device cuda --no-training-video
python -u train.py --method GreedyOffloading --ablation full --device cuda --no-training-video
python -u train.py --method LocalExecution   --ablation full --device cuda --no-training-video
```

Legacy `DMJO` alias run:

```bash
python -u train.py --method DMJO --ablation full --device cuda --no-training-video
```

---

## Ablation Study

Evaluate the contribution of individual framework modules:

```bash
python -u train.py --method MAPPO --ablation full             --device cuda --no-training-video
python -u train.py --method MAPPO --ablation single_timescale --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_mappo_traj    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_coop_cache    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation minimal          --device cuda --no-training-video
```

| Ablation | Mechanism Description |
|---|---|
| `full` | Complete proposed MAPPO-MEC framework |
| `single_timescale` | $K_C = 1$, caching updated every slot without two-timescale separation |
| `no_mappo_traj` | Fixed circular UAV orbits; trajectory is not dynamically learned |
| `no_coop_cache` | Cooperative A2A cache disabled; relies only on local UAV cache and BS backhaul |
| `minimal` | No cooperative cache and plain non-specialized actor policy |

---

## Evaluation

Model evaluation using saved weights:

```bash
python train.py \
  --method MAPPO \
  --ablation full \
  --eval \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --device cuda
```

Custom environment configuration evaluation:

```bash
python test_custom.py \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --num-iot 120 \
  --num-uavs 6 \
  --num-jammers 2 \
  --episodes 20 \
  --device cuda
```

> **Important**: `--checkpoint` in `train.py` is for evaluation mode only. It does not resume training states.

---

## Figures & Plotting

After training metrics have been recorded under `results/`:

```bash
python plot_ieee.py
```

Plots are exported directly to:
```text
results/plots/
```

---

## References

```bibtex
@article{li20263d,
  title   = {3-D Trajectory Design Based on Deep Reinforcement Learning for UAV-Assisted Communication Networks},
  author  = {Li, Meng and Dong, Meng and Wang, Haipeng and Wang, Hong},
  journal = {IEEE Transactions on Network Science and Engineering},
  volume  = {13},
  number  = {1},
  pages   = {248--261},
  year    = {2026},
  doi     = {10.1109/TNSE.2025.3482103}
}
```
