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

LOG_DIR="${PROJECT_ROOT}/experiments/logs"
RESULTS_LOG_DIR="${PROJECT_ROOT}/results/logs"
mkdir -p "${LOG_DIR}" "${RESULTS_LOG_DIR}"

echo "========================================================================"
echo "Executing Baseline 1: GreedyOffloading on ${DEVICE}..."
echo "========================================================================"
python -u train.py --method GreedyOffloading --ablation full --device "${DEVICE}" --no-training-video 2>&1 | tee "${LOG_DIR}/run_greedy.log"
cp "${LOG_DIR}/run_greedy.log" "${RESULTS_LOG_DIR}/run_greedy.log" 2>/dev/null || true

echo "========================================================================"
echo "Executing Baseline 2: LocalExecution on ${DEVICE}..."
echo "========================================================================"
python -u train.py --method LocalExecution --ablation full --device "${DEVICE}" --no-training-video 2>&1 | tee "${LOG_DIR}/run_local.log"
cp "${LOG_DIR}/run_local.log" "${RESULTS_LOG_DIR}/run_local.log" 2>/dev/null || true


echo "All rule-based baseline runs finished successfully."

