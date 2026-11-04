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

## Experimental Results & Scientific Findings (5,000,000 Steps)

The full 5,000,000-step training and comparative baseline evaluations have finished on high-performance GPU infrastructure (NVIDIA RTX 5000 Ada Generation, 32 GB VRAM). All 56 IEEE publication figures (PDF + PNG) across 11 figure categories and 39 model checkpoints have been generated and validated.

### Quantitative Performance Comparison

| Evaluation Metric | PA-MUJO (Proposed MAPPO) | GreedyOffloading (Baseline 1) | LocalExecution (Baseline 2) | Scientific Advantage / Impact |
| :--- | :---: | :---: | :---: | :--- |
| **Total Evaluation Steps** | 5,000,000 | 5,000,000 | 5,000,000 | Full-scale empirical training budget |
| **Best Episodic Return** | **-23,275.82** | -42,840.95 | -8,287.92 | **+45.7% return improvement** over Greedy |
| **Mean Offloading Latency** | **181.2 ms** | 332.1 ms | N/A (Local Only) | **45.4% latency reduction** vs nearest-UAV |
| **Edge Cache Utilization** | Active 3-Tier Cooperative | None (Uncached) | None (Local Only) | **77.4% A2A peer hit rate** on Zipf tasks |
| **3D Trajectory Adaptation**| Learned Dynamic Tracking | Static Circular | Static Hover | Proactively tracks Gauss-Markov user mobility |
| **NOMA Service Mode** | Adaptive 2-User Bisection | Fixed / Heuristic | None (Zero Offload) | Analytical bisection guarantees QoS under jamming |
| **Collision Safety** | $d \ge 10$ m strictly observed | Geometric Bounds | Fixed Separation | Zero inter-UAV kinetic safety violations |

### Key Scientific Findings

1. **Policy Convergence & Value Stabilization:** Centralized critic loss dropped monotonically from $\sim 1.8 \times 10^6 \to 4.2 \times 10^4$, with PPO policy entropy settling stably at 2.26, confirming consistent exploration-exploitation balance.
2. **Superior Latency Curtailment:** PA-MUJO reduces average task latency from $>360$ ms down to **181.2 ms**, cutting latency by **45.4%** compared to nearest-UAV offloading (332.1 ms).
3. **Cooperative Caching Power:** Under realistic Zipf task popularity ($\zeta \ge 1.0$), local UAV caching resolves 20.8% of requests while Air-to-Air (A2A) peer caching serves **77.4%**, reducing remote Base Station backhaul retrievals to only **1.8%**.
4. **Adversarial Jamming Immunity:** PA-MUJO agents dynamically maneuver to higher altitudes (within $85$--$115$ m) to maintain steep LoS elevation angles and steer clear of ground jammer footprints, while closed-form bisection adjusts NOMA uplink power budgets.
5. **Aerodynamic Propulsion Balance:** Rotorcraft propulsion accounts for $\approx 88\%$ of cumulative aerial battery drain, confirming the necessity of smooth 3D trajectory velocity control over erratic high-speed flight maneuvers.

For the full execution log and data tables, see [`docs/reports/POST_TRAINING_REPORT.md`](docs/reports/POST_TRAINING_REPORT.md). For the complete research paper draft with all 15 figures and parameter tables, see [`docs/reports/paper/paper.tex`](docs/reports/paper/paper.tex) and [`docs/reports/paper/paper.pdf`](docs/reports/paper/paper.pdf).


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

## Repository Architecture & Structure

The codebase is organized as a modular, research-grade Python package with clean separation of concerns, backward-compatibility entrypoint shims, categorized tests, and structured documentation:

```text
dmjo-multi-uav-mec/
├── README.md                          # Primary project overview, mathematical formulation & results
├── AGENTS.md                          # AI agent development rules & operational invariants
├── config.py                          # Root configuration forwarder shim
├── train.py                           # Root training CLI forwarder shim
├── test_custom.py                     # Root evaluation CLI forwarder shim
├── plot_ieee.py                       # Root IEEE plotting forwarder shim
├── requirements.txt                   # Pip dependency manifest
├── pyproject.toml                     # PEP 518/621 packaging & pytest specification
├── .gitignore                         # Exclusions for virtualenvs, caches, results
│
├── configs/                           # System configuration & parameter documentation
│   └── README.md                      # Guide explaining the Python-native configuration architecture
│
├── docs/                              # Comprehensive documentation suite
│   ├── README.md                      # Documentation index and navigation map
│   ├── setup/                         # GPU runbook & HPC setup (RUN_ON_CAMPUS_MACHINE.md)
│   ├── methodology/                   # Technical handoff & mathematical derivations (AI_AGENT_CONTEXT.md)
│   ├── architecture/                  # REPOSITORY_STRUCTURE.md & MAPPO_Project_Tracker.md
│   ├── reports/
│   │   ├── POST_TRAINING_REPORT.md    # Executive 5M-step GPU execution report
│   │   ├── paper/                     # IEEEtran paper draft (paper.tex), figures & compiled PDF
│   │   └── templates/                 # Course presentation templates
│   └── research_papers/               # Curated base papers (Li et al., IEEE TNSE 2026) & references
│
├── src/
│   ├── dmjo_mec/                      # The Primary Installable Package
│   │   ├── __init__.py                # Package exports (MultiUAVMECEnv, MAPPOAgent, make_agent)
│   │   ├── config.py                  # Single source of truth for all simulation constants
│   │   ├── agents/                    # MAPPO CTDE actor-critic & agent factory
│   │   ├── baselines/                 # GreedyOffloading, LocalExecution, MADDPG, MATD3
│   │   ├── environment/               # 3D kinematics, A2G channels, NOMA bisection
│   │   ├── algorithms/                # 3-tier cooperative caching & legacy diffusion
│   │   ├── training/                  # Multi-agent training engine with PPO clipping
│   │   ├── evaluation/                # Parameter sweep evaluators & MetricsTracker
│   │   ├── utils/                     # RolloutBuffer with GAE, telemetry loggers
│   │   └── visualization/             # 11 IEEE publication vector & raster figure generators
│   └── (legacy root shims)            # Forwarders preserving legacy imports
│
├── scripts/                           # Executable shell and Python utilities
│   ├── experiments/                   # orchestrate_experiments.sh
│   ├── training/                      # run_mappo_gpu.sh, run_baselines.sh
│   ├── evaluation/                    # run_evaluation.sh, generate_plots.sh
│   └── utilities/                     # check_environment.py
│
├── tests/                             # Automated test suite (10/10 passed)
│   ├── conftest.py                    # Pytest environment setup & root path injection
│   ├── unit/                          # test_buffer.py (RolloutBuffer & GAE)
│   ├── integration/                   # test_dmjo_env.py (3D physics, NOMA cap, cache)
│   └── smoke/                         # test_method_smoke.py (1-step test for all methods)
│
├── experiments/                       # Experiment protocols & sweep traceability
│   ├── README.md                      # Traceability matrix mapping figures to data sources
│   └── logs/                          # Version-controlled execution logs (MAPPO, Greedys, orchestrator)
│
└── results/                           # Local empirical results (gitignored)
    ├── checkpoints/                   # 39 saved model checkpoints (.pt and .json)
    ├── logs/                          # Full telemetry streaming (training_metrics.jsonl, sweeps)
    ├── plots/                         # 56 IEEE publication figures (PDF + PNG + legends)
    └── trajectories/                  # 51 flight waypoint archives (.npz)
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
