#!/usr/bin/env bash
# ==============================================================================
# Script: run_baselines.sh
# Purpose: Execute benchmark baselines (GreedyOffloading and LocalExecution)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${PROJECT_ROOT}"

if [ -f ".venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source ".venv/bin/activate"
fi

DEVICE="${1:-cuda}"

echo "========================================================================"
echo "Executing Baseline 1: GreedyOffloading on ${DEVICE}..."
echo "========================================================================"
python -u train.py --method GreedyOffloading --ablation full --device "${DEVICE}" --no-training-video 2>&1 | tee run_greedy.log

echo "========================================================================"
echo "Executing Baseline 2: LocalExecution on ${DEVICE}..."
echo "========================================================================"
python -u train.py --method LocalExecution --ablation full --device "${DEVICE}" --no-training-video 2>&1 | tee run_local.log

echo "All rule-based baseline runs finished successfully."

