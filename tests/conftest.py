"""Pytest configuration ensuring project root and source modules are on sys.path."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"

for path_str in [str(PROJECT_ROOT), str(SRC_DIR)]:
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
