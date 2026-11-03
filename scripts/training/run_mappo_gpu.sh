#!/usr/bin/env bash
# ==============================================================================
# Script: run_mappo_gpu.sh
# Purpose: Execute full MAPPO multi-UAV MEC training on GPU with tmux
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${PROJECT_ROOT}"

# Activate virtual environment if present
if [ -f ".venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source ".venv/bin/activate"
fi

DEVICE="${1:-cuda}"
METHOD="MAPPO"
ABLATION="full"
STEPS="${2:-5000000}"

echo "========================================================================"
echo "Launching ${METHOD} (${ABLATION}) on ${DEVICE} for ${STEPS} steps..."
echo "========================================================================"

python -u train.py \
    --method "${METHOD}" \
    --ablation "${ABLATION}" \
    --device "${DEVICE}" \
    --total-steps "${STEPS}" \
    --no-training-video 2>&1 | tee run_mappo_full.log
