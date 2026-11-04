# MAPPO Multi-UAV MEC: Final Execution Report

- **Generated At**: 2026-11-04 11:42:19 IST
- **Server Host**: saini (172.20.70.80)
- **GPU**: NVIDIA RTX 5000 Ada Generation (32 GB)

---

## 1. Experimental Results Summary

### A. Primary Method (MAPPO - Full)
- **Method**: MAPPO
- **Ablation**: full (`diffusion=False`)
- **Total Steps**: 5,000,000
- **Log File**: `run_mappo_full.log`
- **Checkpoints**:
  - `results/checkpoints/MAPPO/full/best_model.pt` (12M)
  - `results/checkpoints/MAPPO/full/final_model.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step1000000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step1500000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step2000000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step2500000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step3000000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step3500000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step4000000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step4500000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step5000000.pt` (12M)
  - `results/checkpoints/MAPPO/full/model_step500000.pt` (12M)

### B. Baseline 1 (GreedyOffloading)
- **Method**: GreedyOffloading
- **Log File**: `run_greedy.log`
- **Status**: Completed successfully
- **Checkpoints / Results**:
  - `results/checkpoints/GreedyOffloading/full/best_model.json` (56)
  - `results/checkpoints/GreedyOffloading/full/final_model.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step1000000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step1500000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step2000000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step2500000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step3000000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step3500000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step4000000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step4500000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step5000000.json` (56)
  - `results/checkpoints/GreedyOffloading/full/model_step500000.json` (56)

### C. Baseline 2 (LocalExecution)
- **Method**: LocalExecution
- **Log File**: `run_local.log`
- **Status**: Completed successfully
- **Checkpoints / Results**:
  - `results/checkpoints/LocalExecution/full/best_model.json` (54)
  - `results/checkpoints/LocalExecution/full/final_model.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step1000000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step1500000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step2000000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step2500000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step3000000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step3500000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step4000000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step4500000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step5000000.json` (54)
  - `results/checkpoints/LocalExecution/full/model_step500000.json` (54)

---

## 2. Generated IEEE Plots (`results/plots/`)
Total plots generated: 56
- `results/plots/P1b_latency.pdf` (100K)
- `results/plots/P8_trajectory_legend_step5000000.png` (111K)
- `results/plots/P8_trajectory_legend.png` (111K)
- `results/plots/P1a_reward_legend.png` (11K)
- `results/plots/P7_cache_vs_zipf_legend.pdf` (11K)
- `results/plots/P6_latency_vs_cache.pdf` (13K)
- `results/plots/P7_cache_vs_zipf.pdf` (13K)
- `results/plots/P10_latency_vs_task_size.pdf` (14K)
- `results/plots/P11_latency_vs_tx_power.pdf` (14K)
- `results/plots/P9_latency_vs_jammer_power.pdf` (14K)
- `results/plots/P3_latency_vs_M.pdf` (15K)
- `results/plots/P4_latency_vs_J.pdf` (15K)
- `results/plots/P2_latency_vs_N.pdf` (16K)
- `results/plots/P7_cache_vs_zipf_legend.png` (16K)
- `results/plots/P5_energy.pdf` (18K)
- `results/plots/P8_trajectory_legend_step5000000.pdf` (23K)
- `results/plots/P8_trajectory_legend.pdf` (23K)
- `results/plots/P8_2D_trajectory_step5000000.png` (346K)
- `results/plots/P8_2D_trajectory.png` (346K)
- `results/plots/P7_cache_vs_zipf.png` (35K)
- `results/plots/P10_latency_vs_task_size_legend.pdf` (3.7K)
- `results/plots/P3_latency_vs_M_legend.pdf` (3.7K)
- `results/plots/P3_latency_vs_M.png` (37K)
- `results/plots/P4_latency_vs_J_legend.pdf` (3.7K)
- `results/plots/P6_latency_vs_cache_legend.pdf` (3.7K)
- `results/plots/P9_latency_vs_jammer_power_legend.pdf` (3.7K)
- `results/plots/P11_latency_vs_tx_power_legend.pdf` (3.8K)
- `results/plots/P2_latency_vs_N_legend.pdf` (3.9K)
- `results/plots/P9_latency_vs_jammer_power.png` (39K)
- `results/plots/P6_latency_vs_cache.png` (40K)
- `results/plots/P10_latency_vs_task_size_legend.png` (4.2K)
- `results/plots/P8_3D_trajectory_step5000000.png` (431K)
- `results/plots/P8_3D_trajectory.png` (431K)
- `results/plots/P11_latency_vs_tx_power.png` (43K)
- `results/plots/P3_latency_vs_M_legend.png` (4.3K)
- `results/plots/P10_latency_vs_task_size.png` (45K)
- `results/plots/P4_latency_vs_J_legend.png` (4.5K)
- `results/plots/P6_latency_vs_cache_legend.png` (4.5K)
- `results/plots/P9_latency_vs_jammer_power_legend.png` (4.5K)
- `results/plots/P8_3D_trajectory_step5000000.pdf` (461K)
- `results/plots/P8_3D_trajectory.pdf` (461K)
- `results/plots/P8_2D_trajectory_step5000000.pdf` (464K)
- `results/plots/P8_2D_trajectory.pdf` (464K)
- `results/plots/P11_latency_vs_tx_power_legend.png` (4.7K)
- `results/plots/P2_latency_vs_N_legend.png` (4.7K)
- `results/plots/P1a_reward.png` (53K)
- `results/plots/P1b_latency.png` (53K)
- `results/plots/P5_energy.png` (58K)
- `results/plots/P5_energy_legend.png` (6.9K)
- `results/plots/P5_energy_legend.pdf` (7.4K)
- `results/plots/P2_latency_vs_N.png` (75K)
- `results/plots/P1a_reward_legend.pdf` (7.7K)
- `results/plots/P4_latency_vs_J.png` (77K)
- `results/plots/P1b_latency_legend.pdf` (7.9K)
- `results/plots/P1b_latency_legend.png` (9.8K)
- `results/plots/P1a_reward.pdf` (99K)

---

## 3. Results Archive & Local Transfer

- **Archive File**: `/home/narya/kent-ai/project/dmjo-multi-uav-mec/dmjo_final_results.zip`
- **Archive Size**: 421M
- **SHA-256 Checksum**: `aa18369ffae358f71927f0fa1fd71e2d69b4e84eb7f3bcc5cf1af031fed40cec`

### Windows Download Command (Run in PowerShell or Command Prompt on your local laptop):
```cmd
scp narya@172.20.70.80:/home/narya/dmjo-multi-uav-mec/dmjo_final_results.zip "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec\"
```

### Windows Extraction Command (Run in PowerShell on your local laptop):
```powershell
Expand-Archive -Path "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec\dmjo_final_results.zip" -DestinationPath "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec" -Force
```

---
*Generated automatically by Pipeline Orchestrator.*
