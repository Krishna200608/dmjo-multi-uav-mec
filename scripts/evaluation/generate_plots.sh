#!/usr/bin/env bash
# ==============================================================================
# Script: generate_plots.sh
# Purpose: Generate IEEE publication vector and raster figures from saved logs
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${PROJECT_ROOT}"

if [ -f ".venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source ".venv/bin/activate"
fi

echo "Generating IEEE publication plots (P1a through P11)..."
python plot_ieee.py "$@"

echo "Plots generated in results/plots/ and ready for IEEE paper inclusion."
