"""
DMJO source package.

Submodules are intentionally imported explicitly by callers. Avoiding eager
imports here keeps runtime ablation flags from being captured before train.py
has applied the requested CLI mode.
"""

__all__ = []
