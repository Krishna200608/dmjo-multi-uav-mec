# Repository Architecture & Component Responsibilities

## Overview

The `dmjo-multi-uav-mec` repository implements the **Priority-Aware Multi-UAV Joint Optimization (PA-MUJO)** framework for aerial mobile edge computing. The codebase is organized as a research-grade Python package with separated concerns, full research traceability, comprehensive documentation, and transparent backward-compatibility entrypoints.

---

## Directory Hierarchy

```text
dmjo-multi-uav-mec/
├── README.md                      # Primary project overview, setup, training & evaluation
├── AGENTS.md                      # AI agent operational instructions and interface invariants
├── config.py                      # Root configuration forwarder shim
├── train.py                       # Root training CLI forwarder shim
├── test_custom.py                 # Root evaluation CLI forwarder shim
├── plot_ieee.py                   # Root IEEE plotting forwarder shim
├── requirements.txt               # Pinned Python package dependencies
├── pyproject.toml                 # Standard setuptools packaging & pytest configuration
├── .gitignore                     # Git tracking exclusions
│
├── configs/                       # Configuration documentation & parameter hierarchies
│   └── README.md
│
├── docs/                          # Comprehensive technical and academic documentation
│   ├── README.md                  # Documentation index and navigation map
│   ├── setup/                     # Machine requirements, campus GPU guides, environment setup
│   │   └── RUN_ON_CAMPUS_MACHINE.md
│   ├── methodology/               # Theoretical formulations, CTDE, A2G channels, bisection
│   │   └── AI_AGENT_CONTEXT.md
│   ├── architecture/              # High-level architecture and project trackers
│   │   ├── REPOSITORY_STRUCTURE.md
│   │   └── MAPPO_Project_Tracker.md
│   ├── reports/                   # Publication drafts, experiment summaries, presentation materials
│   │   ├── POST_TRAINING_REPORT.md# Post-training run report and convergence summary
│   │   ├── paper/                 # IEEE paper LaTeX source, bibtex, figures, and compiled PDF
│   │   └── templates/             # Secondary templates and baseline reports
│   └── research_papers/           # Curated scientific literature
│       ├── base_papers/           # Foundational papers on 3D DRL UAV trajectory & MEC
│       └── reference_papers/      # 16 benchmark papers (NOMA, priority, MAPPO, mobility)
│
├── src/                           # Python source tree
│   ├── dmjo_mec/                  # Primary installable package
│   │   ├── __init__.py            # Package root exports (MultiUAVMECEnv, MAPPOAgent, make_agent)
│   │   ├── config.py              # Single source of truth for all simulation constants
│   │   ├── agents/                # MAPPO agent & factory pattern
│   │   │   ├── __init__.py
│   │   │   ├── mappo_agent.py     # CTDE Actor-Critic networks with GAE
│   │   │   └── agent_factory.py   # Method dispatcher (MAPPO, baselines)
│   │   ├── baselines/             # State-of-the-art comparison baselines
│   │   │   ├── __init__.py
│   │   │   ├── greedy_agent.py    # Nearest-UAV heuristic offloading
│   │   │   ├── local_agent.py     # Local device-only execution
│   │   │   ├── maddpg_agent.py    # Multi-Agent DDPG baseline
│   │   │   ├── matd3_agent.py     # Multi-Agent TD3 baseline
│   │   │   └── mappo_baseline.py  # Unablated baseline implementation
│   │   ├── environment/           # Simulation dynamics and physical models
│   │   │   ├── __init__.py
│   │   │   ├── env.py             # 3D kinematics, Gauss-Markov mobility, reward shaping
│   │   │   └── channel_model.py   # Elevation-dependent A2G channels & NOMA bisection
│   │   ├── algorithms/            # Caching and auxiliary algorithms
│   │   │   ├── __init__.py
│   │   │   ├── caching.py         # Two-timescale cooperative edge service caching
│   │   │   └── diffusion.py       # Legacy diffusion actor classes (optional/inactive)
│   │   ├── training/              # Training orchestration
│   │   │   ├── __init__.py
│   │   │   └── train.py           # Core training loop, checkpointing, domain randomization
│   │   ├── evaluation/            # Validation, sweeps, and metric tracking
│   │   │   ├── __init__.py
│   │   │   ├── metrics.py         # MetricsTracker rolling performance logger
│   │   │   └── test_custom.py     # Parameter sweep & generalization tester
│   │   ├── utils/                 # Utilities and buffers
│   │   │   ├── __init__.py
│   │   │   ├── buffer.py          # RolloutBuffer for on-policy PPO updates
│   │   │   └── logger.py          # Metric streaming, JSONL logging & trajectory archiving
│   │   └── visualization/         # Figure generation
│   │       ├── __init__.py
│   │       └── plot_ieee.py       # Standalone IEEE publication plotting suite
│   │
│   └── (legacy shims)             # Backward-compatibility shims forwarding to dmjo_mec.*
│
├── scripts/                       # Executable shell and python scripts
│   ├── experiments/               # Experiment orchestration pipelines
│   │   └── orchestrate_experiments.sh
│   ├── training/                  # Training launch scripts
│   │   ├── run_mappo_gpu.sh
│   │   └── run_baselines.sh
│   ├── evaluation/                # Evaluation & figure scripts
│   │   ├── run_evaluation.sh
│   │   └── generate_plots.sh
│   └── utilities/                 # Diagnostics & health checks
│       └── check_environment.py
│
├── tests/                         # Categorized test suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest path and environment setup
│   ├── unit/                      # Isolated unit tests
│   │   └── test_buffer.py         # Rollout buffer bounds and advantage tests
│   ├── integration/               # Multi-component integration tests
│   │   └── test_dmjo_env.py       # MultiUAVMECEnv step, reset, finite rewards, NOMA
│   └── smoke/                     # End-to-end execution smoke tests
│       └── test_method_smoke.py   # 1-step verification for all 6 methods
│
├── experiments/                   # Experiment protocols, execution logs, and sweeps
│   ├── README.md                  # Experiments overview
│   ├── logs/                      # Version-controlled execution logs (MAPPO, Greedys, orchestrator)
│   │   ├── README.md
│   │   ├── run_mappo_full.log     # 5M-step MAPPO console log
│   │   ├── run_greedy.log         # 5M-step GreedyOffloading console log
│   │   ├── run_local.log          # 5M-step LocalExecution console log
│   │   ├── run_plot.log           # Plotting execution trace
│   │   └── pipeline_orchestrator.log # End-to-end automation trace
│   └── sweeps/
│
├── results/                       # Empirical outputs (gitignored, persisted locally)
│   ├── checkpoints/               # 39 saved model checkpoints (.pt and .json)
│   ├── logs/                      # Full telemetry (training_metrics.jsonl, eval_sweeps.json)
│   ├── plots/                     # 56 IEEE figures + standalone legends (PDF & PNG)
│   └── trajectories/              # 51 3D aerial flight paths (.npz)
│
└── .github/
    └── workflows/
        └── ci.yml                 # Automated syntax & test validation on push/PR
```

---

## Component Responsibilities

1. **`dmjo_mec.environment`**: Implements the continuous physical-world simulation:
   * 3D rotary-wing flight kinodynamics governed by non-linear aerodynamics.
   * Urban elevation-dependent Line-of-Sight (LoS) probabilistic path-loss channels.
   * Gauss-Markov mobile IoT ground devices with stochastic task arrivals.
   * Closed-form golden-section bisection search for optimal NOMA uplink power distribution.
2. **`dmjo_mec.agents`**: Centralized Training with Decentralized Execution (CTDE):
   * Shared parameter Gaussian actor networks receiving normalized local observations.
   * Centralized value critic network with Generalized Advantage Estimation (GAE).
3. **`dmjo_mec.algorithms`**: Sub-tier optimization:
   * Two-timescale cooperative caching across Local UAV cache, Air-to-Air (A2A) peer links, and Base Station (BS).
4. **`dmjo_mec.visualization`**: Generates publication-grade IEEE vector figures with explicit legends and exact metric curves.
