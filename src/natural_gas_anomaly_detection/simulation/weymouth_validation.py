"""Numerical smoke checks for the fluids.compressible.Weymouth API.

These checks verify API compatibility, units, round-trip behavior, and basic
physical ordering. They do NOT establish that the full synthetic gas model,
compressibility assumptions, or leak model are validated for a real pipeline.
"""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from math import isclose, isfinite
from typing import Any

try:
    from fluids.compressible import Weymouth
except ImportError as exc:  # Fail clearly; never replace the library with our own formula.
    raise ImportError(
        "fluids is required for Weymouth validation. Install the project requirements, "
        "then rerun scripts/run_weymouth_validation.py. This project intentionally "
        "does not reimplement the Weymouth equation."
    ) from exc

# Current approved v1 nominal point. These are the configured design baselines,
# not measured BOTAŞ network data. The v1 policy selects fixed Zavg=0.8065;
# OPEN-DECISION-012 remains open only until Colab numerical validation is recorded.
BASELINE: dict[str, float] = {
    "SG": 0.675,
    "Tavg": 283.15,
    "L": 100_000.0,
    "D": 0.75,
    "P1": 9_000_000.0,
    "P2": 5_000_000.0,
    "Ts": 288.15,
    "Ps": 101_325.0,
    "Zavg": 0.8065,
    "E": 0.92,
}

# Value published in the fluids documentation for the exact documented example.
DOCUMENTED_EXAMPLE_Q_M3_S = 32.07729055913029


def fluids_version() -> str:
    """Return the installed fluids distribution version."""
    try:
        return version("fluids")
    except PackageNotFoundError:
        return "unknown"


def run_documented_example() -> dict[str, Any]:
    """Run the official documentation example without overriding its defaults."""
    q = float(
        Weymouth(
            D=0.340,
            P1=90e5,
            P2=20e5,
            L=160e3,
            SG=0.693,
            Tavg=277.15,
        )
    )
    return {
        "name": "fluids_documented_example",
        "Q_m3_s": q,
        "expected_Q_m3_s": DOCUMENTED_EXAMPLE_Q_M3_S,
        "relative_error": abs(q - DOCUMENTED_EXAMPLE_Q_M3_S)
        / DOCUMENTED_EXAMPLE_Q_M3_S,
        "passed": isclose(q, DOCUMENTED_EXAMPLE_Q_M3_S, rel_tol=1e-7, abs_tol=1e-9),
    }


def _call_with_known_flow(*, length_m: float, inlet_pa: float, flow_m3_s: float) -> float:
    """Solve P2 with all physical constants passed explicitly."""
    return float(
        Weymouth(
            SG=BASELINE["SG"],
            Tavg=BASELINE["Tavg"],
            L=length_m,
            D=BASELINE["D"],
            P1=inlet_pa,
            Q=flow_m3_s,
            Ts=BASELINE["Ts"],
            Ps=BASELINE["Ps"],
            Zavg=BASELINE["Zavg"],
            E=BASELINE["E"],
        )
    )


def run_nominal_round_trip() -> dict[str, Any]:
    """Compute nominal flow from P1/P2, then recover P2 from that flow."""
    q0 = float(Weymouth(**BASELINE))
    p2_recovered = _call_with_known_flow(
        length_m=BASELINE["L"], inlet_pa=BASELINE["P1"], flow_m3_s=q0
    )
    relative_error = abs(p2_recovered - BASELINE["P2"]) / BASELINE["P2"]
    return {
        "name": "nominal_pressure_flow_round_trip",
        "Q0_m3_s_at_Ts_Ps": q0,
        "P2_requested_pa": BASELINE["P2"],
        "P2_recovered_pa": p2_recovered,
        "relative_pressure_error": relative_error,
        "passed": (
            isfinite(q0)
            and q0 > 0.0
            and isfinite(p2_recovered)
            and 0.0 < p2_recovered < BASELINE["P1"]
            and isclose(p2_recovered, BASELINE["P2"], rel_tol=1e-8, abs_tol=1e-2)
        ),
    }


def run_demand_bounds_check(q0: float | None = None) -> dict[str, Any]:
    """Check that +/-5% demand yields finite, positive, correctly ordered P2.

    +/-5% is a project design assumption, not a universal pipeline property.
    """
    if q0 is None:
        q0 = float(Weymouth(**BASELINE))
    p2_low_demand = _call_with_known_flow(
        length_m=BASELINE["L"],
        inlet_pa=BASELINE["P1"],
        flow_m3_s=0.95 * q0,
    )
    p2_nominal = _call_with_known_flow(
        length_m=BASELINE["L"],
        inlet_pa=BASELINE["P1"],
        flow_m3_s=q0,
    )
    p2_high_demand = _call_with_known_flow(
        length_m=BASELINE["L"],
        inlet_pa=BASELINE["P1"],
        flow_m3_s=1.05 * q0,
    )
    pressures = (p2_low_demand, p2_nominal, p2_high_demand)
    passed = (
        all(isfinite(p) and 0.0 < p < BASELINE["P1"] for p in pressures)
        and p2_low_demand > p2_nominal > p2_high_demand
    )
    return {
        "name": "plus_minus_5_percent_demand_bounds",
        "demand_multiplier": [0.95, 1.0, 1.05],
        "P2_pa": list(pressures),
        "passed": passed,
        "interpretation": "Higher flow yields lower downstream pressure with other inputs fixed.",
    }


def run_two_segment_leak_sanity_check(q0: float | None = None) -> dict[str, Any]:
    """Run a simplified midpoint leak balance with a fixed Zavg smoke-test value.

    The v1 Zavg policy is fixed at 0.8065 (OPEN-DECISION-012 policy subdecision
    closed). These smoke tests only verify the library API, nominal round-trip,
    and basic numerical behavior. The overall OPEN-DECISION-012 remains open
    until actual Colab outputs are saved and reviewed.
    """
    if q0 is None:
        q0 = float(Weymouth(**BASELINE))
    alpha = 0.10
    q_out = q0
    q_leak = alpha * q_out
    q_in = q_out + q_leak
    half_length = BASELINE["L"] / 2.0
    p_mid = _call_with_known_flow(
        length_m=half_length, inlet_pa=BASELINE["P1"], flow_m3_s=q_in
    )
    p_out = _call_with_known_flow(
        length_m=half_length, inlet_pa=p_mid, flow_m3_s=q_out
    )
    passed = (
        isclose(q_in, q_out + q_leak, rel_tol=0.0, abs_tol=1e-12)
        and all(isfinite(p) and p > 0.0 for p in (p_mid, p_out))
        and BASELINE["P1"] > p_mid > p_out
    )
    return {
        "name": "midpoint_two_segment_leak_sanity_fixed_Zavg",
        "alpha": alpha,
        "Q_in_m3_s": q_in,
        "Q_out_m3_s": q_out,
        "Q_leak_m3_s": q_leak,
        "mass_balance_residual_m3_s": q_in - q_out - q_leak,
        "P_mid_pa": p_mid,
        "P_out_pa": p_out,
        "Zavg_policy": "fixed Zavg=0.8065 selected for v1; Colab numerical validation pending",
        "passed": passed,
    }


def run_all_checks() -> dict[str, Any]:
    """Run all numerical smoke checks and return a serializable report."""
    doc = run_documented_example()
    round_trip = run_nominal_round_trip()
    q0 = round_trip["Q0_m3_s_at_Ts_Ps"]
    demand = run_demand_bounds_check(q0)
    leak = run_two_segment_leak_sanity_check(q0)
    checks = [doc, round_trip, demand, leak]
    return {
        "fluids_version": fluids_version(),
        "baseline_parameters": BASELINE,
        "checks": checks,
        "all_passed": all(bool(item["passed"]) for item in checks),
        "scope_warning": (
            "The v1 Zavg policy is fixed at 0.8065 (OPEN-DECISION-012 policy subdecision closed). "
            "These smoke tests only verify the library API, nominal round-trip, and basic numerical "
            "behavior. The overall OPEN-DECISION-012 remains open until actual Colab outputs are "
            "saved and reviewed."
        ),
    }
