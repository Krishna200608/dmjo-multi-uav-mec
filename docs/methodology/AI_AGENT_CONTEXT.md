# AI Agent Project Context

This file is a technical handoff for any AI coding agent that receives this
repository. It explains the project identity, current implementation, public
interfaces, run commands, known caveats, completed experimental milestones, and the most important files.

---

## 1. One-Sentence Summary

This repository implements the **Priority-Aware Multi-UAV Joint Optimization (PA-MUJO)** framework using MAPPO for joint 3D trajectory control, priority-differentiated task offloading, 3-tier cooperative service caching, and uplink NOMA power allocation in a jammer-aware aerial MEC-IoT network.

---

## 2. Current Project Identity

- **Repository folder:** `dmjo-multi-uav-mec`
- **GitHub remote:** `git@github.com:Krishna200608/dmjo-multi-uav-mec.git`
- **Core Method:** Plain MAPPO under the Centralized Training with Decentralized Execution (CTDE) architecture
- **Analytical Layer:** Analytical convex bisection power allocation for NOMA uplink clusters
- **Primary CLI method:** `MAPPO`
- **Legacy CLI alias:** `DMJO` (backward-compatible forwarder to MAPPO)
- **Inactive/Ablation Code:** Diffusion-related code (`src/dmjo_mec/algorithms/diffusion.py`) remains strictly as optional historical ablation code and is not part of the primary method.

---

## 3. Repository Architecture & Layout

The repository is organized as a research-grade modular Python package:

```text
dmjo-multi-uav-mec/
├── README.md                          # Primary overview, mathematical formulation & results
├── AGENTS.md                          # AI agent development rules & operational invariants
├── config.py                          # Root configuration forwarder shim
├── train.py                           # Root training CLI forwarder shim
├── test_custom.py                     # Root evaluation CLI forwarder shim
├── plot_ieee.py                       # Root IEEE plotting forwarder shim
├── requirements.txt                   # Pip dependency manifest
├── pyproject.toml                     # PEP 518/621 packaging & pytest specification
├── .gitignore                         # Exclusions for virtualenvs, caches, results
│
├── configs/
│   └── README.md                      # Guide to the Python-native configuration architecture
│
├── docs/
│   ├── README.md                      # Documentation index
│   ├── setup/
│   │   └── RUN_ON_CAMPUS_MACHINE.md   # GPU setup, proxy configuration, tmux runbook
│   ├── methodology/
│   │   └── AI_AGENT_CONTEXT.md        # Technical handoff & mathematical derivations
│   ├── architecture/
│   │   ├── REPOSITORY_STRUCTURE.md    # Detailed module breakdown & responsibilities
│   │   └── MAPPO_Project_Tracker.md   # Design decisions & milestone tracking
│   ├── reports/
│   │   ├── POST_TRAINING_REPORT.md    # 5M-step GPU training completion report
│   │   ├── paper/                     # IEEEtran paper LaTeX source, bibtex, figures & PDF
│   │   └── templates/                 # Course presentation templates
│   └── research_papers/
│       ├── base_papers/               # Foundational literature (Li et al., IEEE TNSE 2026)
│       └── reference_papers/          # 16 reference papers (NOMA, priority, MAPPO, mobility)
│
├── src/
│   ├── dmjo_mec/                      # The Primary Installable Package
│   │   ├── __init__.py                # Package exports (MultiUAVMECEnv, MAPPOAgent, make_agent)
│   │   ├── config.py                  # Single source of truth for simulation constants
│   │   ├── agents/                    # MAPPO CTDE actor-critic & agent factory
│   │   ├── baselines/                 # GreedyOffloading, LocalExecution, MADDPG, MATD3
│   │   ├── environment/               # 3D gym-style env, A2G channels, NOMA bisection
│   │   ├── algorithms/                # 3-tier cooperative caching & legacy diffusion
│   │   ├── training/                  # Multi-agent training engine with PPO clipping
│   │   ├── evaluation/                # Parameter sweep evaluators & MetricsTracker
│   │   ├── utils/                     # RolloutBuffer with GAE, telemetry loggers
│   │   └── visualization/             # 11 IEEE publication vector & raster figure generators
│   └── (legacy root shims)            # Forwarders preserving from src.env import ...
│
├── scripts/
│   ├── experiments/                   # orchestrate_experiments.sh
│   ├── training/                      # run_mappo_gpu.sh, run_baselines.sh
│   ├── evaluation/                    # run_evaluation.sh, generate_plots.sh
│   └── utilities/                     # check_environment.py
│
├── tests/
│   ├── conftest.py                    # Pytest environment setup & root path injection
│   ├── unit/                          # test_buffer.py (RolloutBuffer & GAE)
│   ├── integration/                   # test_dmjo_env.py (3D physics, NOMA cap, cache)
│   └── smoke/                         # test_method_smoke.py (1-step test for all methods)
│
├── experiments/
│   ├── README.md                      # Traceability matrix mapping figures to data sources
│   └── logs/                          # Version-controlled execution logs (MAPPO, Greedys, orchestrator)
│
└── results/                           # Local empirical results (gitignored)
    ├── checkpoints/                   # Saved model weights (39 files across MAPPO, Greedys)
    ├── logs/                          # Full telemetry streaming (training_metrics.jsonl, sweeps)
    ├── plots/                         # 56 IEEE publication figures (PDF + PNG + legends)
    └── trajectories/                  # 51 flight waypoint archives (.npz)
```

---

## 4. Core Runtime Flow

```text
train.py (or dmjo_mec.training.train)
  -> config.apply_ablation(args.ablation)
  -> MultiUAVMECEnv(policy_mode=..., ablation_config=...)
  -> make_agent(method=...)
  -> Rollout collection across discrete time slots
  -> Analytical NOMA bisection for power allocation
  -> RolloutBuffer.compute_gae()
  -> MAPPOAgent.update() (PPO clipped surrogate objective + critic value update)
  -> Periodic checkpoints, logs, and trajectories to results/
```

---

## 5. Completed Experimental Milestones (5,000,000 Steps)

All 5,000,000 steps for the primary proposed method and comparison baselines have completed cleanly on NVIDIA RTX 5000 Ada GPU infrastructure:

| Evaluation Metric | MAPPO (Proposed) | GreedyOffloading | LocalExecution | Scientific Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **Total Steps** | 5,000,000 | 5,000,000 | 5,000,000 | Full-budget empirical convergence |
| **Best Return** | **-23,275.82** | -42,840.95 | -8,287.92 | **+45.7% return improvement** over Greedy |
| **Mean Latency** | **181.2 ms** | 332.1 ms | N/A (Local Only) | **45.4% latency reduction** vs nearest-UAV |
| **Edge Caching** | Active 3-Tier | Uncached | Local Only | **77.4% A2A peer hit rate** on Zipf tasks |
| **3D Trajectory** | Learned Tracking | Static Circular | Static Hover | Tracks mobile user centroids adaptively |
| **NOMA Uplink** | Adaptive Bisection | Fixed / Heuristic | None ($0\%$ offload) | Analytical bisection guarantees QoS under jamming |
| **Collision Safety** | $d \ge 10$ m strictly observed | Geometric Bounds | Static Separation | Zero kinetic collision violations |

---

## 6. Verification Commands

```bash
# Diagnostic environment check
python scripts/utilities/check_environment.py

# Syntax & compilation
python -m compileall config.py train.py plot_ieee.py test_custom.py src

# Full pytest test suite (10 tests)
pytest tests -v

# 2-step CPU smoke check
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test

# IEEE plotting test
python plot_ieee.py --env-only --seed 42 --uavs 5 --iot 100 --steps 80
```

---

## 7. Rules for Future AI Agents

- **Truthful Claims:** The project is MAPPO-first; do not describe the core method as diffusion-based.
- **Maintain Modular Invariants:** Add new modules inside `src/dmjo_mec/` and expose them via root shims if backward compatibility is required.
- **No Root Pollution:** Output files, logs, and reports must be saved into `results/`, `experiments/logs/`, or `docs/reports/`—never directly on the project root.
- **Strict Testing:** Always run `pytest tests -v` to ensure 100% test pass rate after modifying environment or agent logic.
