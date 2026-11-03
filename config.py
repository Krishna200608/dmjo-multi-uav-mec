"""
Root configuration module.
Authoritative definitions reside in dmjo_mec.config; this module re-exports
all symbols to preserve backward compatibility with existing scripts.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
for _p in [str(_ROOT), str(_SRC)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dmjo_mec.config import *
import dmjo_mec.config as _cfg

__all__ = [name for name in dir(_cfg) if not name.startswith("__")]
