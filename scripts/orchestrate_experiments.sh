#!/usr/bin/env bash
# Compatibility wrapper for scripts/experiments/orchestrate_experiments.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${SCRIPT_DIR}/experiments/orchestrate_experiments.sh" "$@"

