#!/usr/bin/env bash
# ==============================================================================
# Script: run_evaluation.sh
# Purpose: Evaluate best MAPPO checkpoint across custom environment topologies
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${PROJECT_ROOT}"

if [ -f ".venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source ".venv/bin/activate"
fi

CHECKPOINT="${1:-results/checkpoints/MAPPO/full/best_model.pt}"
DEVICE="${2:-cpu}"

echo "Evaluating model checkpoint: ${CHECKPOINT} on ${DEVICE}..."
python test_custom.py \
    --checkpoint "${CHECKPOINT}" \
    --num-iot 120 \
    --num-uavs 6 \
    --num-jammers 2 \
    --episodes 20 \
    --device "${DEVICE}"
