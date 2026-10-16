#!/usr/bin/env python3
"""Run the fluids-based Weymouth smoke checks and write a JSON report."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from natural_gas_anomaly_detection.simulation.weymouth_validation import run_all_checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports" / "metrics" / "weymouth_validation.json",
        help="Output JSON path. Prefer a persistent Drive path in Colab.",
    )
    args = parser.parse_args()

    report = run_all_checks()
    report["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    report["python_version"] = sys.version
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"\nReport written to: {args.output}")
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
