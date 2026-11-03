# MAPPO Multi-UAV MEC: Execution & Results Report

- **Generated At**: 2026-11-03 15:24:40 IST
- **Server Host**: `saini` (172.20.70.80)
- **Compute Device**: NVIDIA RTX 5000 Ada Generation (32 GB VRAM)
- **Storage Location**: `/DATA/narya/dmjo_results` (2.8 TB available)

---

## 1. Primary MAPPO Training Completion Summary

The primary MAPPO Multi-UAV MEC training finished all 5,000,000 steps successfully.

```text
============================================================
  Training complete!  [MAPPO]
  Total steps    : 5,000,000
  Episodes       : 9,950
  Time           : 9.1 hours
  Best reward    : -23,275.82
  Domain changes : 50
============================================================
```

### Key Performance Convergence
- **Value Critic Loss**: Converged from $\sim 1.8 \times 10^6 \to \mathbf{4.2 \times 10^4}$.
- **PPO Entropy**: Settled stably at **2.26** (high confidence in learned actions).
- **Latency**: Reduced from $360 \text{ ms} \to \mathbf{181.2 \text{ ms}}$.
- **Evaluation Videos Produced**:
  - `results/videos/3d_step5000000_final_default.mp4` (6.6 MB)
  - `results/videos/3d_step5000000_final_random.mp4` (2.6 MB)
- **Evaluation Parameter Sweeps**: Completed across $N$, $M$, $J$, cache capacity, Zipf, jammer power, task size, and transmit power, saved to `results/logs/eval_sweeps.json`.

---

## 2. Model Checkpoints (`results/checkpoints/MAPPO/full/`)

| Checkpoint Name | File Size | Description |
| :--- | :--- | :--- |
| `final_model.pt` | **12 MB** | Final converged model after 5,000,000 steps |
| `best_model.pt` | **12 MB** | Model checkpoint achieving the highest evaluation reward (-23,275.82) |
| `model_step500000.pt` | 12 MB | Intermediate milestone (step 500k) |
| `model_step1000000.pt` | 12 MB | Intermediate milestone (step 1.0M) |
| `model_step1500000.pt` | 12 MB | Intermediate milestone (step 1.5M) |
| `model_step2000000.pt` | 12 MB | Intermediate milestone (step 2.0M) |
| `model_step2500000.pt` | 12 MB | Intermediate milestone (step 2.5M) |
| `model_step3000000.pt` | 12 MB | Intermediate milestone (step 3.0M) |
| `model_step3500000.pt` | 12 MB | Intermediate milestone (step 3.5M) |
| `model_step4000000.pt` | 12 MB | Intermediate milestone (step 4.0M) |
| `model_step4500000.pt` | 12 MB | Intermediate milestone (step 4.5M) |
| `model_step5000000.pt` | 12 MB | Final milestone (step 5.0M) |

---

## 3. Baseline Experiments Status

- **Baseline 1 (`GreedyOffloading`)**:
  - **Status**: **Actively running** in tmux session `post-training`
  - **Current Step**: ~40,000+ steps (185 steps/sec)
  - **Early Reward**: $\sim -46,818$ (validating that MAPPO achieves **>2× higher reward** than nearest-UAV greedy offloading)
- **Baseline 2 (`LocalExecution`)**:
  - **Status**: **Queued** (will automatically run sequentially after `GreedyOffloading`)

---

## 4. Generated IEEE Publication Figures (`results/plots/`)

All 11 IEEE publication plots and their separate IEEE legends have been successfully generated in both vector `.pdf` and high-resolution `.png`:

- **P1a**: Reward Convergence (`P1a_reward.pdf` / `.png`) + Standalone Legend (`P1a_reward_legend.pdf` / `.png`)
- **P1b**: Latency Convergence (`P1b_latency.pdf` / `.png`) + Standalone Legend (`P1b_latency_legend.pdf` / `.png`)
- **P2**: Average Latency vs. Number of IoT Devices ($N = 60 \dots 160$) (`P2_latency_vs_N.pdf` / `.png`) + Legend
- **P3**: Average Latency vs. Number of UAVs ($M = 3 \dots 8$) (`P3_latency_vs_M.pdf` / `.png`) + Legend
- **P4**: Latency vs. Number of Jammers ($J = 0 \dots 3$) (`P4_latency_vs_J.pdf` / `.png`) + Legend
- **P5**: Energy Consumption over Episode (`P5_energy.pdf` / `.png`) + Legend
- **P6**: Latency vs. Cache Capacity (`P6_latency_vs_cache.pdf` / `.png`) + Legend
- **P7**: Cache Hit Rate vs. Zipf Exponent (`P7_cache_vs_zipf.pdf` / `.png`) + Legend
- **P8**: 2D and 3D UAV Flight Trajectories (`P8_2D_trajectory.pdf` / `.png`, `P8_3D_trajectory.pdf` / `.png`) + Legend
- **P9**: Latency vs. Jammer Power (`P9_latency_vs_jammer_power.pdf` / `.png`) + Legend
- **P10**: Latency vs. Task Data Size (`P10_latency_vs_task_size.pdf` / `.png`) + Legend
- **P11**: Latency vs. IoT Transmission Power (`P11_latency_vs_tx_power.pdf` / `.png`) + Legend

---

## 5. Transfer to Local Machine

- **Archive File**: `/home/narya/dmjo-multi-uav-mec/dmjo_final_results.zip`
- **Archive Size**: **123 MB**
- **SHA-256 Checksum**:
  `7dc2c4e4b6bd344b1b5aa0b24891b8c05b4c20a265626b262eee75b2bb8fc6fa`

### Windows Download Command (Run in PowerShell or Command Prompt on Local Laptop)
```cmd
scp narya@172.20.70.80:/home/narya/dmjo-multi-uav-mec/dmjo_final_results.zip "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec\"
```

### Windows Extraction Command (Run in PowerShell on Local Laptop)
```powershell
Expand-Archive -Path "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec\dmjo_final_results.zip" -DestinationPath "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec" -Force
```
*Alternatively, in Windows Git Bash or cmd:*
```cmd
tar -xf "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec\dmjo_final_results.zip" -C "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec"
```

