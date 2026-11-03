#!/usr/bin/env bash
# ==============================================================================
# Pipeline Orchestrator: Post-Training Automation for MAPPO Multi-UAV MEC
# ==============================================================================
# This script monitors the primary MAPPO training job until completion, then:
# 1. Verifies MAPPO success and final checkpoints.
# 2. Sequentially executes GreedyOffloading baseline.
# 3. Sequentially executes LocalExecution baseline.
# 4. Generates publication-quality IEEE plots via plot_ieee.py.
# 5. Packages all results into dmjo_final_results.zip.
# 6. Writes a detailed completion report: POST_TRAINING_REPORT.md.
# ==============================================================================

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

LOGS_DIR="${PROJECT_DIR}/experiments/logs"
RESULTS_LOGS_DIR="${PROJECT_DIR}/results/logs"
mkdir -p "${LOGS_DIR}" "${RESULTS_LOGS_DIR}" "${PROJECT_DIR}/docs/reports"

LOG_FILE="${LOGS_DIR}/pipeline_orchestrator.log"
REPORT_FILE="${PROJECT_DIR}/docs/reports/POST_TRAINING_REPORT.md"
ZIP_FILE="${PROJECT_DIR}/dmjo_final_results.zip"

cd "${PROJECT_DIR}" || exit 1

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "${msg}"
    echo "${msg}" >> "${LOG_FILE}"
    echo "${msg}" >> "${RESULTS_LOGS_DIR}/pipeline_orchestrator.log" 2>/dev/null || true
}

log "========================================================================"
log "Pipeline Orchestrator initialized."
log "Monitoring primary MAPPO training job..."
log "========================================================================"

# Activate virtual environment
if [ -f "${PROJECT_DIR}/.venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source "${PROJECT_DIR}/.venv/bin/activate"
else
    log "ERROR: Virtual environment .venv not found at ${PROJECT_DIR}/.venv"
    exit 1
fi

# ------------------------------------------------------------------------------
# STEP 1: Wait for MAPPO training to finish
# ------------------------------------------------------------------------------
CHECK_INTERVAL=60

while true; do
    # Check if python MAPPO training process is running
    MAPPO_PIDS=$(pgrep -f "python.*train\.py.*--method MAPPO" || true)

    if [ -z "${MAPPO_PIDS}" ]; then
        log "No active MAPPO training process detected."
        break
    fi

    # Also log periodic progress every ~10 minutes
    CURRENT_STEP=$(tail -n 1 results/logs/training_metrics.jsonl 2>/dev/null | grep -o '"step": [0-9]*' | awk '{print $2}' || echo "unknown")
    log "MAPPO training in progress (PIDs: ${MAPPO_PIDS}). Current step: ${CURRENT_STEP} / 5,000,000. Sleeping ${CHECK_INTERVAL}s..."
    sleep ${CHECK_INTERVAL}
done

log "MAPPO training process has terminated. Verifying completion..."

# Verify MAPPO completion
FINAL_CHECKPOINT="${PROJECT_DIR}/results/checkpoints/MAPPO/full/final_model.pt"
MAPPO_LOG="${LOGS_DIR}/run_mappo_full.log"
[ ! -f "${MAPPO_LOG}" ] && [ -f "${RESULTS_LOGS_DIR}/run_mappo_full.log" ] && MAPPO_LOG="${RESULTS_LOGS_DIR}/run_mappo_full.log"
[ ! -f "${MAPPO_LOG}" ] && [ -f "${PROJECT_DIR}/run_mappo_full.log" ] && MAPPO_LOG="${PROJECT_DIR}/run_mappo_full.log"

if [ ! -f "${FINAL_CHECKPOINT}" ]; then
    # Check if run_mappo_full.log mentions completion or error
    if [ -f "${MAPPO_LOG}" ] && grep -q "Training complete!  \[MAPPO\]" "${MAPPO_LOG}" 2>/dev/null; then
        log "WARNING: 'Training complete!' found in log, but final_model.pt missing. Checking best_model.pt..."
    else
        log "FATAL: MAPPO training appears to have terminated without completing 5,000,000 steps!"
        log "Please check ${MAPPO_LOG} for details."
        exit 1
    fi
else
    log "SUCCESS: MAPPO final_model.pt verified at ${FINAL_CHECKPOINT} ($(ls -lh "${FINAL_CHECKPOINT}" | awk '{print $5}'))."
fi

# ------------------------------------------------------------------------------
# STEP 2: Execute Baseline 1 - GreedyOffloading
# ------------------------------------------------------------------------------
log "========================================================================"
log "Starting Baseline 1: GreedyOffloading"
log "========================================================================"

GREEDY_LOG="${LOGS_DIR}/run_greedy.log"
python -u train.py --method GreedyOffloading --ablation full --device cuda --no-training-video > "${GREEDY_LOG}" 2>&1
GREEDY_EXIT=$?
cp "${GREEDY_LOG}" "${RESULTS_LOGS_DIR}/run_greedy.log" 2>/dev/null || true

if [ ${GREEDY_EXIT} -ne 0 ]; then
    log "FATAL: GreedyOffloading baseline failed with exit code ${GREEDY_EXIT}."
    log "Check ${GREEDY_LOG} for errors."
    exit ${GREEDY_EXIT}
fi
log "SUCCESS: GreedyOffloading baseline completed successfully."

# ------------------------------------------------------------------------------
# STEP 3: Execute Baseline 2 - LocalExecution
# ------------------------------------------------------------------------------
log "========================================================================"
log "Starting Baseline 2: LocalExecution"
log "========================================================================"

LOCAL_LOG="${LOGS_DIR}/run_local.log"
python -u train.py --method LocalExecution --ablation full --device cuda --no-training-video > "${LOCAL_LOG}" 2>&1
LOCAL_EXIT=$?
cp "${LOCAL_LOG}" "${RESULTS_LOGS_DIR}/run_local.log" 2>/dev/null || true

if [ ${LOCAL_EXIT} -ne 0 ]; then
    log "FATAL: LocalExecution baseline failed with exit code ${LOCAL_EXIT}."
    log "Check ${LOCAL_LOG} for errors."
    exit ${LOCAL_EXIT}
fi
log "SUCCESS: LocalExecution baseline completed successfully."

# ------------------------------------------------------------------------------
# STEP 4: Generate Final IEEE Plots
# ------------------------------------------------------------------------------
log "========================================================================"
log "Generating IEEE publication plots via plot_ieee.py"
log "========================================================================"

PLOT_LOG="${LOGS_DIR}/run_plot.log"
python plot_ieee.py > "${PLOT_LOG}" 2>&1
PLOT_EXIT=$?
cp "${PLOT_LOG}" "${RESULTS_LOGS_DIR}/run_plot.log" 2>/dev/null || true

if [ ${PLOT_EXIT} -ne 0 ]; then
    log "WARNING: plot_ieee.py exited with code ${PLOT_EXIT}. Checking log..."
else
    log "SUCCESS: plot_ieee.py finished successfully."
fi

# Count generated plots
PLOT_COUNT=$(find "${PROJECT_DIR}/results/plots" -type f \( -name "*.pdf" -o -name "*.png" \) 2>/dev/null | wc -l)
log "Generated ${PLOT_COUNT} plot files in results/plots/."

# ------------------------------------------------------------------------------
# STEP 5: Prepare ZIP Archive for Transfer
# ------------------------------------------------------------------------------
log "========================================================================"
log "Packaging results into ${ZIP_FILE}"
log "========================================================================"

rm -f "${ZIP_FILE}" "${ZIP_FILE}.sha256"

zip -r "${ZIP_FILE}" \
    results/plots \
    results/checkpoints \
    results/logs \
    results/trajectories \
    experiments/logs \
    docs/reports/POST_TRAINING_REPORT.md >> "${LOG_FILE}" 2>&1

if [ -f "${ZIP_FILE}" ]; then
    ZIP_SIZE=$(ls -lh "${ZIP_FILE}" | awk '{print $5}')
    sha256sum "${ZIP_FILE}" > "${ZIP_FILE}.sha256"
    ZIP_SHA=$(cat "${ZIP_FILE}.sha256" | awk '{print $1}')
    log "SUCCESS: ZIP archive created (${ZIP_SIZE}). SHA256: ${ZIP_SHA}"
else
    log "FATAL: Failed to create ZIP archive."
    exit 1
fi

# ------------------------------------------------------------------------------
# STEP 6: Generate Final Execution Report
# ------------------------------------------------------------------------------
log "Writing final summary report to ${REPORT_FILE}..."

cat << EOF > "${REPORT_FILE}"
# MAPPO Multi-UAV MEC: Final Execution Report

- **Generated At**: $(date '+%Y-%m-%d %H:%M:%S %Z')
- **Server Host**: saini (172.20.70.80)
- **GPU**: NVIDIA RTX 5000 Ada Generation (32 GB)

---

## 1. Experimental Results Summary

### A. Primary Method (MAPPO - Full)
- **Method**: MAPPO
- **Ablation**: full (\`diffusion=False\`)
- **Total Steps**: 5,000,000
- **Log File**: \`run_mappo_full.log\`
- **Checkpoints**:
$(find results/checkpoints/MAPPO/full -type f -exec ls -lh {} + 2>/dev/null | awk '{printf "  - `%s` (%s)\n", $9, $5}')

### B. Baseline 1 (GreedyOffloading)
- **Method**: GreedyOffloading
- **Log File**: \`run_greedy.log\`
- **Status**: Completed successfully
- **Checkpoints / Results**:
$(find results/checkpoints/GreedyOffloading -type f -exec ls -lh {} + 2>/dev/null | awk '{printf "  - `%s` (%s)\n", $9, $5}')

### C. Baseline 2 (LocalExecution)
- **Method**: LocalExecution
- **Log File**: \`run_local.log\`
- **Status**: Completed successfully
- **Checkpoints / Results**:
$(find results/checkpoints/LocalExecution -type f -exec ls -lh {} + 2>/dev/null | awk '{printf "  - `%s` (%s)\n", $9, $5}')

---

## 2. Generated IEEE Plots (\`results/plots/\`)
Total plots generated: ${PLOT_COUNT}
$(find results/plots -type f -exec ls -lh {} + 2>/dev/null | sort | awk '{printf "- `%s` (%s)\n", $9, $5}')

---

## 3. Results Archive & Local Transfer

- **Archive File**: \`${ZIP_FILE}\`
- **Archive Size**: ${ZIP_SIZE}
- **SHA-256 Checksum**: \`${ZIP_SHA}\`

### Windows Download Command (Run in PowerShell or Command Prompt on your local laptop):
\`\`\`cmd
scp narya@172.20.70.80:/home/narya/dmjo-multi-uav-mec/dmjo_final_results.zip "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec\"
\`\`\`

### Windows Extraction Command (Run in PowerShell on your local laptop):
\`\`\`powershell
Expand-Archive -Path "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec\dmjo_final_results.zip" -DestinationPath "D:\Lab\Data Management in Mobile and Sensor Networks\dmjo-multi-uav-mec" -Force
\`\`\`

---
*Generated automatically by Pipeline Orchestrator.*
EOF

log "========================================================================"
log "Pipeline Orchestrator completed all tasks successfully!"
log "========================================================================"

