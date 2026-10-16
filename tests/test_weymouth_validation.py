"""Integration checks requiring the real fluids dependency.

When fluids is unavailable, pytest skips this test locally. In Colab Phase 3,
fluids is installed from requirements.txt and this test must execute (not skip).
"""
import pytest

pytest.importorskip("fluids", reason="Install requirements.txt to run real Weymouth checks")

from natural_gas_anomaly_detection.simulation.weymouth_validation import run_all_checks


def test_real_fluids_weymouth_numerical_smoke_checks():
    report = run_all_checks()
    failed = [item for item in report["checks"] if not item["passed"]]
    assert not failed, f"Weymouth validation failures: {failed}"
    assert report["all_passed"] is True
