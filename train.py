#!/usr/bin/env python3
"""
CLI entrypoint for training MAPPO and baseline models in Multi-UAV MEC.
Delegates to dmjo_mec.training.train.main().
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
for p in [str(PROJECT_ROOT), str(SRC_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from dmjo_mec.training.train import main

if __name__ == "__main__":
    main()
