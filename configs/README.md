# DMJO-MEC Configuration System

This directory documents and organizes the configuration architecture for the **Priority-Aware Multi-UAV Joint Optimization (PA-MUJO)** framework.

## Architecture

To ensure high performance, numerical precision, and GPU reproducibility without overhead from external parser dependencies, all system parameters and hyperparameters are maintained natively in Python.

* **Canonical Engine**: [`src/dmjo_mec/config.py`](../src/dmjo_mec/config.py)
* **Root Compatibility Layer**: [`config.py`](../config.py) (re-exports all symbols for backward compatibility with root CLI scripts)

---

## Parameter Categories

### 1. Spatial Topology & Network Architecture
* `AREA_RADIUS`: Surveillance area radius ($500$ m).
* `NUM_UAVS`: Active rotary-wing UAV aerial servers ($J = 5$).
* `MIN_UAVS`, `MAX_UAVS`: Bounds on fleet size ($3 \le J \le 8$).
* `NUM_USERS`: Terrestrial IoT ground devices ($I = 100$).
* `UAV_ALTITUDE_MIN`, `UAV_ALTITUDE_MAX`: Flight altitude envelope ($[80, 120]$ m).
* `UAV_SPEED_MAX`: Maximum horizontal flight speed ($25$ m/s).
* `D_MIN_UAV`: Collision avoidance safety distance ($30$ m).

### 2. Physical-Layer Wireless Channel & NOMA
* `CARRIER_FREQ`: Transmission carrier frequency ($2.0$ GHz).
* `BANDWIDTH`: Total system bandwidth ($10$ MHz).
* `NOISE_POWER_SPECTRAL_DENSITY`: Thermal noise spectral density ($-130$ dBm/Hz).
* `IOT_TX_POWER_MAX`: Maximum device transmit power ($23$ dBm / $200$ mW).
* `NOMA_MAX_CLUSTER_SIZE`: Bound on concurrent NOMA multiplexing ($S_{\max} = 2$).
* `QOS_RATE_THRESHOLD`: Minimum rate for transmission feasibility ($10^5$ bps).

### 3. Task Generation & Composite Priority Model
* `TASK_SIZE_MIN`, `TASK_SIZE_MAX`: Workload data payload ($[0.5, 5.0]$ Mbits).
* `TASK_CYCLES_MIN`, `TASK_CYCLES_MAX`: Required CPU cycles ($[0.1, 1.0] \times 10^9$ cycles).
* `TASK_DEADLINE_MIN`, `TASK_DEADLINE_MAX`: Latency deadline margins ($[0.2, 2.0]$ s).
* `TASK_ARRIVAL_PROB`: Poisson arrival probability ($0.7$).
* `PRIORITY_MU_URGENCY`: Weight for deadline urgency ($\mu_u = 0.5$).
* `PRIORITY_MU_CRITICALITY`: Weight for semantic criticality ($\mu_c = 0.5$).
* `PENALTY_DEADLINE_VIOLATION`: Reward penalty multiplier ($2.0$).

### 4. Rotary-Wing Aerodynamic Propulsion
* `BLADE_PROFILE_POWER_P0`: Hover profile power ($79.86$ W).
* `INDUCED_POWER_PI`: Hover induced power ($88.63$ W).
* `ROTOR_TIP_SPEED_UTIP`: Tip velocity ($120$ m/s).
* `MEAN_ROTOR_INDUCED_SPEED_V0`: Mean induced speed ($4.03$ m/s).
* `FUSELAGE_DRAG_RATIO_D0`: Fuselage drag coefficient ($0.6$).
* `ROTOR_DISC_AREA`: Rotor actuator area ($0.503 \text{ m}^2$).

### 5. Multi-Agent RL & MAPPO Hyperparameters
* `TOTAL_TIMESTEPS`: Total training horizon ($5,000,000$ steps).
* `ROLLOUT_LENGTH`: PPO rollout buffer horizon ($500$ steps).
* `MINIBATCH_SIZE`: Optimization batch size ($100$ steps).
* `PPO_EPOCHS`: Policy optimization epochs per update ($10$).
* `LR_ACTOR`, `LR_CRITIC`: Actor ($3 \times 10^{-4}$) and Critic ($1 \times 10^{-4}$) learning rates.
* `MAPPO_GAMMA`: Temporal discount factor ($\gamma = 0.99$).
* `MAPPO_GAE_LAMBDA`: Generalized Advantage Estimation parameter ($\lambda = 0.95$).
* `PPO_CLIP_EPS`: Surrogate clipping margin ($\epsilon = 0.2$).

---

## Runtime Ablation Resolver

Ablations are applied dynamically via `apply_ablation(name)`:
* `full`: Standard PA-MUJO framework (learned 3D trajectory + cooperative caching + non-diffusion MAPPO).
* `single_timescale`: Cache updated every step ($K_C = 1$).
* `no_mappo_traj`: UAVs follow static circular flight orbits.
* `no_coop_cache`: Local execution and terrestrial BS only (no A2A cache tier).
* `minimal`: Plain MAPPO actor without cooperative cache.
