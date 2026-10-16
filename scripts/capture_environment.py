#!/usr/bin/env python3
"""Write a reproducibility manifest for the active Python environment."""
from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ["numpy", "pandas", "scipy", "scikit-learn", "torch", "fluids", "PyYAML", "pytest"]


def main() -> None:
    package_versions = {}
    for package in PACKAGES:
        try:
            package_versions[package] = version(package)
        except PackageNotFoundError:
            package_versions[package] = None

    torch_info = {"available": False, "cuda_available": False, "cuda_version": None}
    try:
        import torch

        torch_info = {
            "available": True,
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda,
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        }
    except ImportError:
        pass

    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "packages": package_versions,
        "torch_runtime": torch_info,
    }
    output = ROOT / "reports" / "metrics" / "phase3_environment_manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"Manifest written to: {output}")


if __name__ == "__main__":
    main()
