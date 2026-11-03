#!/usr/bin/env python3
"""
CLI entrypoint for generating IEEE publication figures.
Delegates to dmjo_mec.visualization.plot_ieee.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
for p in [str(PROJECT_ROOT), str(SRC_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dmjo_mec.visualization.plot_ieee import (
    generate_trajectory_plots,
    generate_final_trajectory_plots,
    main,
)

if __name__ == "__main__":
    main()
