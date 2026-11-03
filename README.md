# Priority-Aware Task Offloading and 3D Trajectory Optimization in NOMA-Enabled Multi-UAV MEC-IoT Networks Using MAPPO

Cooperative Multi-Agent Proximal Policy Optimization (MAPPO) framework for joint 3D trajectory control, priority-aware computation offloading, cooperative service caching, and uplink Non-Orthogonal Multiple Access (NOMA) in heterogeneous aerial edge computing networks.

---

## Overview

In massive Internet of Things (IoT) deployments, resource-constrained ground devices (GDs) generate heterogeneous computation workloads ranging from delay-tolerant background telemetry to latency-critical robotic control and emergency signaling. Traditional terrestrial edge networks struggle with sparse infrastructure and fixed coverage bottlenecks.

This repository provides an autonomous multi-UAV mobile edge computing (MEC) platform where a fleet of rotary-wing unmanned aerial vehicles (UAVs) equipped with edge compute servers and wireless transceivers provides on-demand computing and communication services to mobile ground devices.

The optimization framework operates under the **Centralized Training with Decentralized Execution (CTDE)** paradigm using **Multi-Agent Proximal Policy Optimization (MAPPO)**. To resolve the joint continuous-discrete dimensionality curse, the framework establishes a **hybrid analytical-RL decoupling**: decentralized MAPPO actors steer macro-level spatial navigation and offloading association, while uplink NOMA transmit powers and Successive Interference Cancellation (SIC) decoding orders are resolved analytically.

```
                      +------------------------------------------+
                      |      Centralized Critic (Global State)   |
                      +--------------------+---------------------+
                                           | GAE & Advantage
                                           v
       +-----------------------------------+-----------------------------------+
       |                                   |                                   |
+------v------------------+       +--------v----------------+       +----------v--------------+
|   UAV Actor 1 (Local)   |       |   UAV Actor 2 (Local)   |       |   UAV Actor J (Local)   |
| 3D Velocity & Offloading|       | 3D Velocity & Offloading|       | 3D Velocity & Offloading|
+------+------------------+       +--------+----------------+       +----------+--------------+
       |                                   |                                   |
       | 3D Navigation                     | 3D Navigation                     | 3D Navigation
       v                                   v                                   v
+---------------------------------------------------------------------------------------------+
|                  Uplink NOMA Power Allocation (Closed-Form Convex Bisection)                 |
+---------------------------------------------------------------------------------------------+
       ^                                   ^                                   ^
       |                                   |                                   |
  [GD Group 1]                       [GD Group 2]                        [GD Group I]
  (Priority: Urgency + Criticality; Gauss-Markov Mobility; Elevation-Dependent LoS/NLoS Links)
```

---

## Base Research & Architectural Evolution

This system builds upon and expands the physical and mathematical foundation of:

> **Base Literature:**  
> Min Li, Miao Dong, Hong Wang, and Heng Wang, *"3-D Trajectory Design Based on Deep Reinforcement Learning for UAV-Assisted Communication Networks"*, **IEEE Transactions on Network Science and Engineering**, vol. 13, pp. 10551–10571, 2026.  
> DOI: [10.1109/TNSE.2026.3715712](https://doi.org/10.1109/TNSE.2026.3715712)  
> *Document location: `docs/research_papers/base_papers/3-D_Trajectory_Design_Based_on_Deep_Reinforcement_Learning_for_UAV-Assisted_Communication_Networks.pdf`*

### System Dimension Comparison

| Feature Dimension | Base Work (Li et al., *IEEE TNSE* 2026) | This Implementation (PA-MUJO Framework) |
|---|---|---|
| **Fleet Topology** | Single UAV aerial communication relay | **Heterogeneous Multi-UAV Fleet** ($J \ge 5$) with diverse compute, cache, and battery profiles |
| **Learning Paradigm** | Single-agent continuous RL (PKTD3-TD) | **Multi-Agent PPO (MAPPO)** with CTDE, GAE, and clipped surrogate objectives |
| **Compute Layer** | None (pure data relaying) | **Two-Tier MEC**: Local IoT execution vs. Aerial UAV edge processing with queue backlog evolution |
| **Workload Urgency** | Uniform / Agnostic | **Composite Urgency-Criticality Prioritization** ($\Omega_i[t]$) preventing priority inversion |
| **Multiple Access** | Orthogonal Multiple Access (OMA / TDMA) | **Power-Domain Uplink NOMA** with SIC and analytical bisection power allocation |
| **Channel Model** | Probabilistic A2G LoS/NLoS links | **Elevation-dependent A2G probabilistic channels** with Rician fading and dynamic Doppler shifts |
| **Aerodynamics** | Non-linear rotary-wing propulsion power | **Analytical rotary-wing propulsion** (blade profile, induced power, parasitic drag) + flight budgets |
| **Safety Guarantees**| Boundary enforcement | **Strict inter-UAV collision distance** ($d_{\min}$), altitude limits ($z_{\min}, z_{\max}$), and flight envelopes |
| **Objective** | Network throughput maximization | **Priority-weighted latency minimization** regularized by fleet energy consumption |

---

## Core System Modules

### 1. Priority-Aware Workload Modeling
To eliminate **priority inversion**—where delay-tolerant telemetry monopolizes edge buffers and starves mission-critical requests—each task $i$ is governed by a dynamic composite priority weight $\Omega_i[t] \in (0, 1]$:

$$\Omega_i[t] = \mu_u \Omega_i^{\mathrm{urg}}[t] + \mu_c \Omega_i^{\mathrm{cls}}[t]$$

- **Dynamic Urgency $\Omega_i^{\mathrm{urg}}[t]$:** Exponential function of the remaining deadline margin:
  $$\Omega_i^{\mathrm{urg}}[t] = \exp\left(-\frac{\tau_i^{\max}[t] - \Delta t_i[t]}{\tau_i^{\max}[t]}\right)$$
- **Application Criticality $\Omega_i^{\mathrm{cls}}[t]$:** Discrete semantic classes reflecting operational criticality (e.g., class 1: background telemetry $\omega=0.2$; class 4: safety-critical actuation $\omega=1.0$).
- **Normalized System Metric:** The optimization minimizes the priority-weighted average latency:
  $$\bar{T}_{\mathrm{pri}}[t] = \frac{\sum_{i \in \mathcal{I}} \Omega_i[t] T_i^{\mathrm{task}}[t]}{\sum_{i \in \mathcal{I}} \Omega_i[t]}$$

### 2. 3D UAV Kinematics & Aerodynamic Propulsion
Each UAV $j \in \mathcal{J}$ navigates in continuous 3D space with position $\mathbf{p}_j[t] = [x_j[t], y_j[t], z_j[t]]^\top$. Propulsion power follows the non-linear rotary-wing aerodynamic model:

$$P_j^{\mathrm{prop}}[t] = P_0 \left(1 + \frac{3 v_j^2[t]}{U_{\mathrm{tip}}^2}\right) + P_i \left(\sqrt{1 + \frac{v_j^4[t]}{4 v_0^4}} - \frac{v_j^2[t]}{2 v_0^2}\right)^{1/2} + \frac{1}{2} d_0 \rho_{\mathrm{air}} s_{\mathrm{rotor}} A_{\mathrm{rotor}} v_j^3[t]$$

Kinematic safety constraints enforce:
- Velocity envelope: $\|\mathbf{p}_j[t+1] - \mathbf{p}_j[t]\|_2 \le V_{\max} \delta$
- Altitude bounds: $z_{\min} \le z_j[t] \le z_{\max}$
- Collision avoidance: $\|\mathbf{p}_j[t] - \mathbf{p}_{j'}[t]\|_2 \ge d_{\min}, \quad \forall j \neq j'$

### 3. NOMA-Enhanced Uplink Transmission & SIC
Ground devices offloading to the same UAV in time slot $t$ share bandwidth via power-domain NOMA:
- Multiplexing cluster cap: $|\mathcal{S}_j[t]| \le S_{\max} = 2$.
- Successive Interference Cancellation (SIC): Received signals are decoded sequentially in ascending order of effective channel gains.
- Transmit Power Allocation: Conditionally optimized via analytical convex bisection, guaranteeing QoS rate thresholds while eliminating continuous power variables from the RL policy.

### 4. Air-to-Ground Probabilistic Propagation
Elevation angle $\theta_{i,j}[t] = \frac{180}{\pi} \arcsin\left(\frac{z_j[t]}{d_{i,j}[t]}\right)$ dictates the Line-of-Sight probability:

$$\mathbb{P}^{\mathrm{LoS}}_{i,j}[t] = \frac{1}{1 + a \exp\left(-b \left[\theta_{i,j}[t] - a\right]\right)}$$

Total path loss combines free-space propagation with excess LoS/NLoS attenuation and Rician small-scale fading.

### 5. Ground Device Mobility
Mobile ground terminals follow the Gauss-Markov mobility model with memory parameters $\alpha_v, \alpha_\varphi \in [0, 1]$, simulating correlated vehicular and robotic movement across the service zone.

---

## Multi-Agent Decision Process (MAMDP)

### Observation & State Spaces
- **Local Observation $\mathbf{o}_j[t] \in \mathcal{O}_j$ (Decentralized Actor):**  
  Own 3D coordinates, velocity vector, remaining battery fraction, local edge queue backlog, channel gains to candidate ground devices, composite priority weights of nearby tasks, and relative displacement vectors to neighboring UAVs within sensing range.
- **Global State $\mathbf{s}[t] \in \mathcal{S}$ (Centralized Critic):**  
  Concatenation of all UAV positions, velocities, battery levels, complete ground device locations, channel state matrices, and global queue backlogs across the entire fleet.

### Action Space
Each UAV agent outputs a 5-D continuous action vector $\mathbf{a}_j[t] \in [-1, 1]^5$:
- $a_{j,1}, a_{j,2}, a_{j,3}$: Continuous 3D displacement adjustments ($\Delta x, \Delta y, \Delta z$).
- $a_{j,4}$: Offloading mode preference bias (local-first vs. edge offloading).
- $a_{j,5}$: NOMA device scheduling selection hint.

### Multi-Objective Reward Function
The team reward balances latency minimization, energy frugality, and physical safety:

$$r_j[t] = -\left( \bar{T}_{\mathrm{pri}}[t] + \lambda_{\mathrm{eng}} E_j^{\mathrm{total}}[t] + \lambda_{\mathrm{col}} \Pi_j^{\mathrm{col}}[t] + \lambda_{\mathrm{bnd}} \Pi_j^{\mathrm{bnd}}[t] + \lambda_{\mathrm{ddl}} \Pi_j^{\mathrm{ddl}}[t] \right)$$

where $\Pi_j^{\mathrm{col}}$, $\Pi_j^{\mathrm{bnd}}$, and $\Pi_j^{\mathrm{ddl}}$ represent penalty functions for collision violations, territory border exceedances, and deadline expiration events.

---

## Repository Layout

```text
dmjo-multi-uav-mec/
|-- AGENTS.md                  # Development guidelines & environment context
|-- README.md                  # Project documentation & system specification
|-- config.py                  # Physical parameters, network settings, and hyperparameters
|-- train.py                   # Main distributed training & evaluation pipeline
|-- test_custom.py             # Custom environment scenario evaluation
|-- plot_ieee.py               # IEEE publication-quality plotting script
|-- requirements.txt           # Python dependency specifications
|-- docs/
|   |-- AI_AGENT_CONTEXT.md    # Technical architectural context
|   |-- MAPPO_Project_Tracker.md# Implementation roadmap & status
|   |-- RUN_ON_CAMPUS_MACHINE.md# Multi-node HPC execution guide
|   `-- Base Paper/            # Reference PDF (Li et al., IEEE TNSE 2026)
|-- tests/
|   |-- test_buffer.py         # Rollout buffer & GAE unit tests
|   |-- test_dmjo_env.py       # Physical simulation & channel model tests
|   `-- test_method_smoke.py   # Multi-agent baseline smoke tests
`-- src/
    |-- __init__.py
    |-- env.py                 # Multi-UAV MEC vector environment & physics
    |-- mappo_agent.py         # MAPPO Actor-Critic with CTDE & GAE
    |-- channel_model.py       # Probabilistic A2G channels & NOMA SIC
    |-- caching.py             # 3-tier cooperative edge caching logic
    |-- buffer.py              # Centralized/decentralized experience replay buffer
    |-- metrics.py             # QoS, priority latency, & energy trackers
    |-- logger.py              # TensorBoard & console logging utilities
    |-- agent_factory.py       # Factory interface for MAPPO & baselines
    |-- diffusion.py           # Optional legacy ablation baseline
    `-- baselines/             # Benchmark suite
        |-- maddpg_agent.py    # Multi-Agent Deep Deterministic Policy Gradient
        |-- matd3_agent.py     # Multi-Agent Twin Delayed DDPG
        |-- greedy_agent.py    # Priority-heuristic greedy offloading
        `-- local_agent.py     # Local-only computation baseline
```

---

## Repository Structure

The codebase is organized as a modular, research-grade Python package with separated concerns:

```text
dmjo-multi-uav-mec/
├── src/dmjo_mec/                  # Primary installable package
│   ├── agents/                    # MAPPO agent & factory
│   ├── baselines/                 # Comparison agents (Greedy, Local, MADDPG, MATD3)
│   ├── environment/               # Physical 3D kinematics, A2G channels, NOMA bisection
│   ├── algorithms/                # Cooperative caching & diffusion models
│   ├── training/                  # Core training pipeline
│   ├── evaluation/                # MetricsTracker & custom evaluation
│   ├── utils/                     # Rollout buffers & training loggers
│   └── visualization/             # IEEE publication plotting suite
├── configs/                       # System configuration & parameter documentation
├── docs/                          # Architecture, methodology, setup, reports & papers
│   ├── setup/                     # GPU runbook (RUN_ON_CAMPUS_MACHINE.md)
│   ├── methodology/               # Full mathematical technical handoff
│   ├── architecture/              # REPOSITORY_STRUCTURE.md & tracker
│   ├── reports/paper/             # IEEE paper LaTeX draft & figures
│   └── research_papers/           # Base papers & reference literature
├── scripts/                       # Executable runners for training, evaluation, utilities
├── tests/                         # Unit, integration, and smoke tests
├── experiments/                   # Experiment protocols & sweep traceability
└── results/                       # Trained models (.pt), logs (.jsonl), IEEE plots
```
For a detailed component-by-component breakdown, see [`docs/architecture/REPOSITORY_STRUCTURE.md`](docs/architecture/REPOSITORY_STRUCTURE.md).

---

## Installation & Setup

### Prerequisites
- Python 3.10 or newer (tested on Python 3.10 and 3.11)
- CUDA 11.8+ / 12.X (optional, for GPU acceleration)

### Virtual Environment Setup

**Linux / macOS:**
```bash
git clone git@github.com:Krishna200608/dmjo-multi-uav-mec.git
cd dmjo-multi-uav-mec
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Windows PowerShell:**
```powershell
cd "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec"
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Verification & Testing

Verify that the environment physics, buffers, and all agents execute properly:

```bash
# Run unit test suite
pytest tests -v

# Run 2-step CPU smoke test
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

---

## Training

### Proposed Method (MAPPO)

Train the complete proposed framework with continuous 3D navigation, NOMA, priority offloading, and cooperative caching:

```bash
# GPU training (recommended)
python -u train.py --method MAPPO --ablation full --device cuda --no-training-video

# CPU training
python -u train.py --method MAPPO --ablation full --device cpu --no-training-video
```

Default training length: `TOTAL_TIMESTEPS = 5,000,000`. Checkpoints and logs are saved automatically to `results/`.

### Benchmark Baselines

Train comparative baselines under identical environmental conditions:

```bash
# Multi-Agent Continuous RL Baselines
python -u train.py --method MADDPG           --ablation full --device cuda --no-training-video
python -u train.py --method MATD3            --ablation full --device cuda --no-training-video

# Heuristic & Classical Baselines
python -u train.py --method GreedyOffloading --ablation full --device cuda --no-training-video
python -u train.py --method LocalExecution   --ablation full --device cuda --no-training-video
```

---

## Ablation Study

Evaluate the performance impact of individual architectural components:

```bash
# Full proposed system
python -u train.py --method MAPPO --ablation full             --device cuda --no-training-video

# Ablation 1: Single timescale (caching updated every time slot without timescale separation)
python -u train.py --method MAPPO --ablation single_timescale --device cuda --no-training-video

# Ablation 2: Fixed circular trajectory (no dynamic 3D velocity optimization)
python -u train.py --method MAPPO --ablation no_mappo_traj    --device cuda --no-training-video

# Ablation 3: No cooperative A2A cache sharing (local UAV cache + BS backhaul only)
python -u train.py --method MAPPO --ablation no_coop_cache    --device cuda --no-training-video

# Ablation 4: Minimal baseline (no cooperative caching, plain actor)
python -u train.py --method MAPPO --ablation minimal          --device cuda --no-training-video
```

---

## Evaluation & Metrics

Evaluate trained policy checkpoints:

```bash
# Standard evaluation
python train.py \
  --method MAPPO \
  --ablation full \
  --eval \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --device cuda

# Custom network scale testing
python test_custom.py \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --num-iot 120 \
  --num-uavs 6 \
  --num-jammers 2 \
  --episodes 20 \
  --device cuda
```

### Result Visualization
Generate publication-ready comparison curves and 3D trajectory plots:

```bash
python plot_ieee.py
```
Outputs are saved to `results/plots/`.

---

## Key Configuration Parameters

System defaults defined in `config.py`:

| Parameter | Symbol | Value | Description |
|---|---|---|---|
| `AREA_RADIUS` | $R_{\mathrm{cov}}$ | 500 m | Circular operational zone radius |
| `NUM_UAVS` | $J$ | 5 | Default number of UAV edge servers |
| `NUM_USERS` | $I$ | 100 | Default number of active ground IoT devices |
| `ALTITUDE_MIN` | $z_{\min}$ | 80 m | Minimum permissible flight altitude |
| `ALTITUDE_MAX` | $z_{\max}$ | 130 m | Maximum permissible flight altitude |
| `MAX_VELOCITY` | $V_{\max}$ | 20 m/s | Maximum UAV horizontal flight speed |
| `COLLISION_DIST` | $d_{\min}$ | 10 m | Minimum inter-UAV separation safety threshold |
| `NOMA_CLUSTER_CAP` | $S_{\max}$ | 2 | Maximum multiplexed devices per UAV subchannel |
| `SLOT_DURATION` | $\delta$ | 1.0 s | Discrete time step interval |
| `TOTAL_TIMESTEPS` | - | 5,000,000 | Total environment steps per training run |

---

## Base Literature Reference

```bibtex
@article{li2026tnse,
  author   = {Li, Min and Dong, Miao and Wang, Hong and Wang, Heng},
  title    = {{3-D Trajectory Design Based on Deep Reinforcement Learning for UAV-Assisted Communication Networks}},
  journal  = {IEEE Transactions on Network Science and Engineering},
  volume   = {13},
  pages    = {10551--10571},
  year     = {2026},
  doi      = {10.1109/TNSE.2026.3715712}
}
```
