#!/usr/bin/env python3
"""
CLI entrypoint for custom environment evaluation and scaling sweeps.
Delegates to dmjo_mec.evaluation.test_custom.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
for p in [str(PROJECT_ROOT), str(SRC_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dmjo_mec.evaluation.test_custom import main

if __name__ == "__main__":
    main()
