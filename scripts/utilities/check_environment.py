#!/usr/bin/env python3
"""
Environment diagnostic and GPU verification utility.
Checks Python version, PyTorch installation, CUDA acceleration, and critical dependencies.
"""
import sys
import platform
from pathlib import Path

def check_env():
    print("=" * 60)
    print("DMJO-MEC Environment Verification Utility")
    print("=" * 60)
    print(f"Platform       : {platform.platform()}")
    print(f"Python Version : {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"Executable     : {sys.executable}")
    
    # Check PyTorch & CUDA
    try:
        import torch
        print(f"PyTorch Version: {torch.__version__}")
        cuda_avail = torch.cuda.is_available()
        print(f"CUDA Available : {cuda_avail}")
        if cuda_avail:
            device_count = torch.cuda.device_count()
            print(f"CUDA Devices   : {device_count}")
            for i in range(device_count):
                props = torch.cuda.get_device_properties(i)
                print(f"  Device {i}     : {props.name} ({props.total_memory / (1024**3):.1f} GB VRAM)")
        else:
            print("  Notice       : CPU execution only (GPU acceleration unavailable)")
    except ImportError:
        print("ERROR: PyTorch (torch) is not installed in current environment!")

    # Check key dependencies
    packages = ["numpy", "matplotlib", "imageio"]
    for pkg in packages:
        try:
            mod = __import__(pkg)
            ver = getattr(mod, "__version__", "installed")
            print(f"{pkg.capitalize():15}: {ver}")
        except ImportError:
            print(f"ERROR: {pkg} is not installed!")

    # Check package import
    try:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
        SRC_DIR = PROJECT_ROOT / "src"
        for p in [str(PROJECT_ROOT), str(SRC_DIR)]:
            if p not in sys.path:
                sys.path.insert(0, p)
        import dmjo_mec
        print(f"dmjo_mec Package: Version {dmjo_mec.__version__} (Loaded successfully)")
    except Exception as e:
        print(f"WARNING: dmjo_mec import check failed: {e}")

    print("=" * 60)
    print("Verification completed cleanly.")
    print("=" * 60)

if __name__ == "__main__":
    check_env()

