# Running MAPPO Multi-UAV MEC on the Campus Machine

This is the runbook for producing final project results on the campus machine.
The final method is MAPPO-based, not diffusion-based.

Repository:

```text
git@github.com:Krishna200608/dmjo-multi-uav-mec.git
```

Project folder:

```text
dmjo-multi-uav-mec
```

Do not train the older `uav_trajectory_rl` folder for final results.

## 1. Important Method Update

Use this command family for final results:

```bash
python train.py --method MAPPO ...
```

Do not present the project as diffusion-based.

Compatibility notes:

- `MAPPO` is the main method and default.
- `DMJO` is only a backward-compatible alias for the MAPPO path.
- `--ablation no_diffusion` is a compatibility label only; the full MAPPO method
  is already non-diffusion.
- Old checkpoints/plots from diffusion-labelled runs are stale.

## 2. Machine Requirements

Minimum:

- Python 3.10 or newer. Python 3.11 is recommended.
- Enough disk space for `results/`.
- CPU-only runs work, but full training will be slow.

Recommended:

- NVIDIA GPU with CUDA.
- Recent NVIDIA driver.
- `tmux` or `screen` for long unattended runs.

Check GPU:

```bash
nvidia-smi
```

Check PyTorch CUDA after environment setup:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO CUDA')"
```

Expected for GPU training:

```text
True
<GPU name>
```

If CUDA is unavailable, use `--device cpu`.

## 3. Get the Code

Clone fresh on the campus machine:

```bash
mkdir -p ~/dmjo
cd ~/dmjo
git clone git@github.com:Krishna200608/dmjo-multi-uav-mec.git
cd dmjo-multi-uav-mec
```

If SSH is not configured on that machine, use HTTPS instead:

```bash
git clone https://github.com/Krishna200608/dmjo-multi-uav-mec.git
```

## 4. Create the Python Environment

### Linux venv

```bash
cd ~/dmjo/dmjo-multi-uav-mec
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the campus network requires the proxy:

```bash
export HTTP_PROXY=http://172.31.2.4:8080
export HTTPS_PROXY=http://172.31.2.4:8080

python -m pip install --upgrade pip --proxy http://172.31.2.4:8080
python -m pip install -r requirements.txt --proxy http://172.31.2.4:8080
```

### Conda alternative

```bash
conda create -n mappo-uav python=3.11 -y
conda activate mappo-uav
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### CUDA PyTorch

If `pip install -r requirements.txt` installs a CPU-only PyTorch build, install
the CUDA build that matches the campus machine. Use the official PyTorch selector
for the exact CUDA version.

Example for many CUDA 12.1 systems:

```bash
python -m pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu121
```

With proxy:

```bash
python -m pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu121 --proxy http://172.31.2.4:8080
```

Then verify CUDA:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## 5. Quick Verification

Run tests:

```bash
python -m pytest tests -q
```

Expected:

```text
10 passed
```

Run a tiny MAPPO smoke test:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cuda --no-training-video --smoke-test
```

CPU fallback:

```bash
python train.py --method MAPPO --ablation full --total-steps 2 --device cpu --no-training-video --smoke-test
```

Expected signs:

- It prints `Agent: MAPPO`.
- It prints `diffusion=False`.
- It prints `Training complete!`.
- It prints `Total steps    : 2`.

## 6. Medium Sanity Run

Before a full run, do a medium sanity run:

```bash
python -u train.py \
  --method MAPPO \
  --ablation full \
  --total-steps 50000 \
  --device cuda \
  --no-training-video
```

Check outputs:

```text
results/checkpoints/MAPPO/full/
results/logs/MAPPO/full/training_log.jsonl
results/logs/training_metrics.jsonl
results/trajectories/
```

## 7. Full Main Training Run

Default full training budget:

```text
TOTAL_TIMESTEPS = 5,000,000
```

Run:

```bash
python -u train.py \
  --method MAPPO \
  --ablation full \
  --device cuda \
  --no-training-video
```

Output:

```text
results/checkpoints/MAPPO/full/
results/logs/MAPPO/full/
```

Important files:

```text
best_model.pt
final_model.pt
model_step*.pt
```

## 8. Baseline Comparison Runs

Run these fresh for final comparison:

```bash
python -u train.py --method MAPPO            --ablation full --device cuda --no-training-video
python -u train.py --method MADDPG           --ablation full --device cuda --no-training-video
python -u train.py --method MATD3            --ablation full --device cuda --no-training-video
python -u train.py --method GreedyOffloading --ablation full --device cuda --no-training-video
python -u train.py --method LocalExecution   --ablation full --device cuda --no-training-video
```

Output folders:

```text
results/checkpoints/MAPPO/full/
results/checkpoints/MADDPG/full/
results/checkpoints/MATD3/full/
results/checkpoints/GreedyOffloading/full/
results/checkpoints/LocalExecution/full/
```

`GreedyOffloading` and `LocalExecution` are rule-based and should be much
cheaper to run.

## 9. Ablation Runs

Use these for the final ablation study:

```bash
python -u train.py --method MAPPO --ablation full             --device cuda --no-training-video
python -u train.py --method MAPPO --ablation single_timescale --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_mappo_traj    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation no_coop_cache    --device cuda --no-training-video
python -u train.py --method MAPPO --ablation minimal          --device cuda --no-training-video
```

Compatibility-only run:

```bash
python -u train.py --method MAPPO --ablation no_diffusion --device cuda --no-training-video
```

Do not use `no_diffusion` as a final scientific ablation, because the main
method is already non-diffusion.

## 10. Long-Run Pattern With tmux

```bash
tmux new -s mappo-uav
cd ~/dmjo/dmjo-multi-uav-mec
source .venv/bin/activate
bash scripts/training/run_mappo_gpu.sh cuda 5000000
```

Detach:

```text
Ctrl-b then d
```

Reattach:

```bash
tmux attach -t mappo-uav
```

Choose a GPU if multiple are available:

```bash
CUDA_VISIBLE_DEVICES=0 python -u train.py --method MAPPO --ablation full --device cuda --no-training-video
```

## 11. Monitoring

Training log:

```bash
tail -f results/logs/MAPPO/full/training_log.jsonl
```

Terminal log:

```bash
tail -f experiments/logs/run_mappo_full.log
```

GPU:

```bash
watch -n 2 nvidia-smi
```

Watch for:

- Increasing total steps.
- Checkpoints saved under `results/checkpoints/<method>/<ablation>/`.
- No `nan`, `inf`, CUDA out-of-memory, or shape errors.
- `diffusion=False` in startup logs.

## 12. Evaluation

Evaluate the best MAPPO model:

```bash
python train.py \
  --method MAPPO \
  --ablation full \
  --eval \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --device cuda
```

Evaluate the final MAPPO model:

```bash
python train.py \
  --method MAPPO \
  --ablation full \
  --eval \
  --checkpoint results/checkpoints/MAPPO/full/final_model.pt \
  --device cuda
```

Custom environment evaluation:

```bash
python test_custom.py \
  --checkpoint results/checkpoints/MAPPO/full/best_model.pt \
  --num-iot 120 \
  --num-uavs 6 \
  --num-jammers 2 \
  --episodes 20 \
  --device cuda
```

Important: `--checkpoint` in `train.py` is evaluation-only. Training does not
resume optimizer/model state from a checkpoint automatically.

## 13. Generate Figures

```bash
python plot_ieee.py
```

Expected output:

```text
results/plots/
```

## 14. What to Bring Back

Copy back:

```text
results/checkpoints/
results/logs/
results/plots/
results/test_results/
results/trajectories/
experiments/logs/
```

Most important:

```text
results/checkpoints/MAPPO/full/best_model.pt
results/checkpoints/MAPPO/full/final_model.pt
results/logs/MAPPO/full/training_log.jsonl
results/plots/
```

## 15. Troubleshooting

CUDA not detected:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

If `nvidia-smi` works but PyTorch says `False`, install a CUDA-enabled PyTorch
build.

CUDA out of memory:

- Close other GPU jobs.
- Use a different GPU with `CUDA_VISIBLE_DEVICES`.
- Run one method at a time.
- Keep `--no-training-video`.

Interrupted run:

- Current training does not automatically resume from `model_step*.pt`.
- Use `best_model.pt` or `final_model.pt` for evaluation.
- Start a fresh run if the training run was interrupted too early.

Inconsistent results:

- Archive old `results/` before fresh runs.
- Check command uses `--method MAPPO`.
- Check the checkpoint path matches `results/checkpoints/MAPPO/<ablation>/`.
- Re-run `python -m pytest tests -q`.

## 16. Minimal Command Checklist

```bash
cd ~/dmjo/dmjo-multi-uav-mec
source .venv/bin/activate
python -m pytest tests -q
python train.py --method MAPPO --ablation full --total-steps 2 --device cuda --no-training-video --smoke-test
bash scripts/training/run_mappo_gpu.sh cuda 5000000
python plot_ieee.py
```
