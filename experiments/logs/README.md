# Execution and Pipeline Logs

This directory contains version-controlled runtime execution logs, console output captures, and pipeline orchestration records.

---

## Log File Catalog

| Log File | Generating Process | Purpose & Contents |
| :--- | :--- | :--- |
| `run_mappo_full.log` | `scripts/training/run_mappo_gpu.sh` / `train.py` | Complete stdout/stderr trace from the 5,000,000-step primary MAPPO training run on NVIDIA RTX 5000 Ada GPU (9.1 hours, 9,950 episodes, convergence telemetry). |
| `run_greedy.log` | `scripts/training/run_baselines.sh` / `train.py` | Stdout/stderr trace from the `GreedyOffloading` baseline evaluation comparing heuristic nearest-UAV offloading against MAPPO. |
| `pipeline_orchestrator.log` | `scripts/experiments/orchestrate_experiments.sh` | Execution trace of the post-training automation monitor, including milestone verification, baseline dispatching, plot generation, and archive compression. |

---

## Runtime vs. Version-Controlled Logs

* **`experiments/logs/`** (this directory): Tracked in git for immediate reproducibility and inspection by reviewers without downloading large binary archives.
* **`results/logs/`**: Local runtime storage for high-volume streaming telemetry (`training_metrics.jsonl`), per-episode reward records (`training_log.jsonl`), cache analytics (`cache_stats.jsonl`), and parameter sweep matrices (`eval_sweeps.json`).
