# Experiments & Results Traceability

This directory documents the experimental protocols, parameter sweeps, and the exact traceability chain linking experiment runs to the generated IEEE publication figures.

---

## 1. Directory Organization

* **`experiments/logs/`**: Version-controlled console outputs and pipeline execution logs:
  * `run_mappo_full.log`: Console stdout/stderr stream from primary training run.
  * `run_greedy.log`: Console log from greedy baseline run.
  * `pipeline_orchestrator.log`: End-to-end automation orchestration trace.
* **`results/checkpoints/`**: Trained neural network weights (.pt).
  * `MAPPO/full/best_model.pt`: Model achieving highest episodic evaluation reward (-23,275.82).
  * `MAPPO/full/final_model.pt`: Converged model checkpoint at 5,000,000 steps.
  * `MAPPO/full/model_step*.pt`: Periodic milestone checkpoints every 500,000 steps.
  * `GreedyOffloading/`: Baseline checkpoints.
* **`results/logs/`**:
  * `MAPPO/full/training_log.jsonl`: Complete 5-million step per-episode logs across 9,950 episodes.
  * `eval_sweeps.json`: Structured empirical evaluation sweeps across parameter axes.
  * `training_metrics.jsonl`: Step-by-step metric telemetry streaming.
* **`results/plots/`**: Vector `.pdf` and high-resolution `.png` figures generated for publication.
* **`results/trajectories/`**: 3D waypoint coordinate archives (.npz) logged during evaluation.

---

## 2. Research Traceability Matrix

| IEEE Plot | Paper Reference | Metric / Evaluation Axis | Source Log / Data Key |
| :--- | :--- | :--- | :--- |
| **P1a** | Fig. 4 (Convergence) | Episode Return ($5 \times 10^6$ steps) | `results/logs/MAPPO/full/training_log.jsonl` |
| **P1b** | Fig. 4 (Latency) | Average Task Latency Convergence | `results/logs/MAPPO/full/training_log.jsonl` |
| **P2** | Fig. 5 (Scaling) | Latency vs. IoT Population ($N = 60 \dots 160$) | `eval_sweeps.json["P2"]` |
| **P3** | Multi-UAV Scaling | Latency vs. UAV Fleet Size ($M = 3 \dots 8$) | `eval_sweeps.json["P3"]` |
| **P4** | Jammer Immunity | Latency vs. Jammers ($J = 0 \dots 3$) | `eval_sweeps.json["P4"]` |
| **P5** | Fig. 6 (Energy) | Cumulative Fleet Energy Consumption | `results/logs/training_metrics.jsonl` |
| **P6** | Cache Impact | Latency vs. Storage Capacity | `eval_sweeps.json["P6"]` |
| **P7** | Request Skewness | Cache Hit Rate vs. Zipf Exponent | `eval_sweeps.json["P7"]` |
| **P8** | 2D / 3D Kinematics | Converged Trajectories & Safe Separation | `results/trajectories/flight_path_*.npz` |
| **P9** | Robustness | Latency vs. Jammer Power ($15 \dots 25$ dBm) | `eval_sweeps.json["P9"]` |
| **P10** | Workload Scale | Latency vs. Task Data Size ($0.5 \dots 5.0$ Mb)| `eval_sweeps.json["P10"]` |
| **P11** | Transmit Power | Latency vs. Ground Device Power ($15 \dots 23$ dBm)| `eval_sweeps.json["P11"]` |

---

## 3. Reproduction Commands

To reproduce the full set of figures from saved logs:
```bash
python plot_ieee.py
```

To evaluate a specific checkpoint on a custom environment configuration:
```bash
python test_custom.py --checkpoint results/checkpoints/MAPPO/full/best_model.pt --num-iot 120 --num-uavs 6
```

