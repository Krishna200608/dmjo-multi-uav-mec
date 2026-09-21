# Running DMJO on the Campus Machine

This document is the runbook for training and evaluating the final DMJO codebase on a machine with stronger compute than the laptop. The project to run is:

```text
Diffusion_DRL_MultiUAV-DMJO
```

The older `uav_trajectory_rl` folder is only a verified reference project. Do not train that folder for the final DMJO results.

## 1. What Changed Before This Run

The DMJO code was recently corrected so the main runtime behavior now matches the final project plan:

- Per-UAV action is 5D: `[dx, dy, dh, offload_bias, schedule_hint]`.
- NOMA serves at most two selected IoT devices per UAV per slot.
- Runtime ablations now actually affect actor construction, cache lookup, trajectory mode, and macro timescale.
- `GreedyOffloading` and `LocalExecution` now use explicit environment policy modes.
- PPO rollout updates no longer train on zero-padded partial rollouts.
- New tests pass in the local environment.

Because of these changes, any previous DMJO checkpoints/results should be treated as stale. Fresh training runs are required.

## 2. Machine Requirements

Minimum:

- Python 3.10 or newer.
- Enough disk space for `results/` checkpoints, logs, plots, and videos.
- CPU-only runs work but will be very slow for full training.

Recommended:

- NVIDIA GPU with CUDA.
- Recent NVIDIA driver.
- `tmux` or `screen` for long unattended runs.

Check GPU availability:

```bash
nvidia-smi
```

Check PyTorch CUDA from inside the project environment:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO CUDA')"
```

Expected for GPU training:

```text
True
<GPU name>
```

If CUDA is not available, use `--device cpu`, but expect long training time.

## 3. Copy the Project to the Campus Machine

Copy the full folder:

```text
Diffusion_DRL_MultiUAV-DMJO
```

Recommended destination example:

```bash
~/dmjo/Diffusion_DRL_MultiUAV-DMJO
```

Before training, move into the project:

```bash
cd ~/dmjo/Diffusion_DRL_MultiUAV-DMJO
```

Do not rely on old `results/` contents. If old results exist, archive them separately before starting fresh runs.

## 4. Create the Python Environment

### Option A: venv

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install PyTorch with CUDA if the default install does not provide CUDA. Use the command recommended by the official PyTorch selector for the campus machine CUDA version.

Example for many CUDA 12.x systems:

```bash
pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu121
```

Then verify:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

### Option B: conda

```bash
conda create -n dmjo python=3.10 -y
conda activate dmjo
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install a CUDA-enabled PyTorch build if needed, then verify CUDA as above.

## 5. Quick Verification Before Long Training

Run the test suite:

```bash
python -m pytest tests -q
```

Expected:

```text
10 passed
```

Run a very short smoke test on GPU:

```bash
python train.py --method DMJO --ablation full --total-steps 2 --device cuda --no-training-video --smoke-test
```

If there is no CUDA GPU:

```bash
python train.py --method DMJO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

Expected signs:

- It prints `Agent: DMJO`.
- It prints `Training complete!`.
- It prints `Total steps : 2`.

## 6. Medium Sanity Run

Before spending many hours/days, run a medium sanity run:

```bash
python -u train.py \
  --method DMJO \
  --ablation full \
  --total-steps 50000 \
  --device cuda \
  --no-training-video
```

Check that these folders/files appear:

```text
results/checkpoints/DMJO/full/
results/logs/DMJO/full/training_log.jsonl
results/logs/training_metrics.jsonl
results/trajectories/
```

Note: `--no-training-video` skips periodic mid-training videos. Final videos/plots/sweeps may still run at the end unless `--smoke-test` is used.

## 7. Full Training Commands

The default full training budget is:

```text
TOTAL_TIMESTEPS = 5,000,000
```

Main DMJO run:

```bash
python -u train.py \
  --method DMJO \
  --ablation full \
  --device cuda \
  --no-training-video
```

Output path:

```text
results/checkpoints/DMJO/full/
results/logs/DMJO/full/
```

Important checkpoint files:

```text
best_model.pt
final_model.pt
model_step*.pt
```

## 8. Full Comparison Runs

Run all six methods fresh if comparison plots/tables are needed:

```bash
python -u train.py --method DMJO             --ablation full --device cuda --no-training-video
python -u train.py --method MAPPO            --ablation full --device cuda --no-training-video
python -u train.py --method MADDPG           --ablation full --device cuda --no-training-video
python -u train.py --method MATD3            --ablation full --device cuda --no-training-video
python -u train.py --method GreedyOffloading --ablation full --device cuda --no-training-video
python -u train.py --method LocalExecution   --ablation full --device cuda --no-training-video
```

Output folders:

```text
results/checkpoints/DMJO/full/
results/checkpoints/MAPPO/full/
results/checkpoints/MADDPG/full/
results/checkpoints/MATD3/full/
results/checkpoints/GreedyOffloading/full/
results/checkpoints/LocalExecution/full/
```

Rule-based methods are much cheaper, but running them through the same CLI keeps logs and outputs consistent.

## 9. Ablation Runs

For the DMJO ablation study:

```bash
python -u train.py --method DMJO --ablation full             --device cuda --no-training-video
python -u train.py --method DMJO --ablation single_timescale --device cuda --no-training-video
python -u train.py --method DMJO --ablation no_diffusion     --device cuda --no-training-video
python -u train.py --method DMJO --ablation no_mappo_traj    --device cuda --no-training-video
python -u train.py --method DMJO --ablation no_coop_cache    --device cuda --no-training-video
python -u train.py --method DMJO --ablation minimal          --device cuda --no-training-video
```

Output folders:

```text
results/checkpoints/DMJO/full/
results/checkpoints/DMJO/single_timescale/
results/checkpoints/DMJO/no_diffusion/
results/checkpoints/DMJO/no_mappo_traj/
results/checkpoints/DMJO/no_coop_cache/
results/checkpoints/DMJO/minimal/
```

## 10. Recommended Long-Run Pattern

Use `tmux`:

```bash
tmux new -s dmjo
cd ~/dmjo/Diffusion_DRL_MultiUAV-DMJO
source .venv/bin/activate
python -u train.py --method DMJO --ablation full --device cuda --no-training-video 2>&1 | tee run_dmjo_full.log
```

Detach:

```text
Ctrl-b then d
```

Reattach:

```bash
tmux attach -t dmjo
```

If multiple GPUs are available, select one:

```bash
CUDA_VISIBLE_DEVICES=0 python -u train.py --method DMJO --ablation full --device cuda --no-training-video
```

## 11. Monitoring Training

In another terminal:

```bash
tail -f results/logs/DMJO/full/training_log.jsonl
```

Or monitor the terminal log if using `tee`:

```bash
tail -f run_dmjo_full.log
```

Watch for:

- Increasing total steps.
- Checkpoints saved under `results/checkpoints/<method>/<ablation>/`.
- No `nan`, `inf`, CUDA out-of-memory, or shape errors.
- Reasonable latency/reward movement over time.

GPU monitoring:

```bash
watch -n 2 nvidia-smi
```

## 12. Evaluation

Evaluate a trained model with `train.py --eval`.

Example for DMJO full:

```bash
python train.py \
  --method DMJO \
  --ablation full \
  --eval \
  --checkpoint results/checkpoints/DMJO/full/best_model.pt \
  --device cuda
```

For final model:

```bash
python train.py \
  --method DMJO \
  --ablation full \
  --eval \
  --checkpoint results/checkpoints/DMJO/full/final_model.pt \
  --device cuda
```

Custom environment evaluation:

```bash
python test_custom.py \
  --checkpoint results/checkpoints/DMJO/full/best_model.pt \
  --num-iot 120 \
  --num-uavs 6 \
  --num-jammers 2 \
  --episodes 20 \
  --device cuda
```

Important: `--checkpoint` in `train.py` is currently for evaluation mode only. The training loop does not resume optimizer/model state from a checkpoint automatically.

## 13. Generate Figures

After training/evaluation data exists:

```bash
python plot_ieee.py
```

Expected output:

```text
results/plots/
```

Plots are saved as `.png` and `.pdf` where supported by the plotting script.

## 14. What to Bring Back From the Campus Machine

Copy back at least:

```text
results/checkpoints/
results/logs/
results/plots/
results/test_results/
results/trajectories/
run_*.log
```

The most important files are:

```text
results/checkpoints/<method>/<ablation>/best_model.pt
results/checkpoints/<method>/<ablation>/final_model.pt
results/logs/<method>/<ablation>/training_log.jsonl
results/plots/*.png
results/plots/*.pdf
```

## 15. Troubleshooting

### CUDA is not detected

Run:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

If `nvidia-smi` works but PyTorch says `False`, install a CUDA-enabled PyTorch wheel.

### CUDA out of memory

Try:

- Close other GPU jobs.
- Use a different GPU via `CUDA_VISIBLE_DEVICES`.
- Run one method at a time.
- Reduce plotting/video generation by using `--no-training-video`.

### Run interrupted

Current training does not automatically resume from `model_step*.pt`. Keep terminal logs and use `best_model.pt` / `final_model.pt` for evaluation. If a full training run is interrupted early, start a fresh run or add resume support before relying on continuation.

### Results look inconsistent

Make sure:

- Old `results/` were archived before fresh runs.
- The command used the intended `--method` and `--ablation`.
- Evaluation checkpoint path matches the method/ablation folder.
- `python -m pytest tests -q` passes on the campus machine.

## 16. Minimal Command Checklist

```bash
cd ~/dmjo/Diffusion_DRL_MultiUAV-DMJO
source .venv/bin/activate
python -m pytest tests -q
python train.py --method DMJO --ablation full --total-steps 2 --device cuda --no-training-video --smoke-test
python -u train.py --method DMJO --ablation full --device cuda --no-training-video 2>&1 | tee run_dmjo_full.log
python plot_ieee.py
```

