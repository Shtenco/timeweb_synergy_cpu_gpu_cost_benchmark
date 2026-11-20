"""Cost calculator with explicit caller-supplied assumptions, not live tariffs."""

from __future__ import annotations

import math


def estimate_cost(
    hourly_cost: float,
    requests_per_second: float,
    utilization: float,
    success_rate: float,
    hours: float,
) -> dict:
    try:
        hourly_cost, requests_per_second, utilization, success_rate, hours = (
            float(value) for value in (hourly_cost, requests_per_second, utilization, success_rate, hours)
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("all calculator inputs must be numeric") from exc
    values = (hourly_cost, requests_per_second, utilization, success_rate, hours)
    if any(not math.isfinite(value) for value in values):
        raise ValueError("all calculator inputs must be finite")
    if any(value < 0 for value in values):
        raise ValueError("cost, rate, utilization, success rate and hours must be nonnegative")
    if hourly_cost < 0 or requests_per_second <= 0 or hours <= 0:
        raise ValueError("hourly_cost must be nonnegative; rate and hours must be positive")
    if not 0 < utilization <= 1 or not 0 <= success_rate <= 1:
        raise ValueError("utilization must be in (0, 1] and success_rate in [0, 1]")
    total_cost = hourly_cost * hours
    total_requests = requests_per_second * utilization * hours * 3600
    correct_answers = total_requests * success_rate
    per_thousand = (total_cost / correct_answers * 1000) if correct_answers else None
    return {
        "hourly_cost_input": float(hourly_cost),
        "requests_per_second": float(requests_per_second),
        "utilization": float(utilization),
        "success_rate": float(success_rate),
        "hours": float(hours),
        "total_cost": round(total_cost, 8),
        "estimated_requests": round(total_requests, 4),
        "estimated_correct_answers": round(correct_answers, 4),
        "cost_per_1000_correct": round(per_thousand, 8) if per_thousand is not None else None,
    }


def run(seed: int = 42) -> dict:
    assumptions = {"hourly_cost": 1.0, "requests_per_second": 5.0, "utilization": 0.35, "success_rate": 0.82, "hours": 24.0}
    return {
        "evidence_type": "computed",
        "seed": seed,
        "assumptions": assumptions,
        "estimate": estimate_cost(**assumptions),
        "limitations": [
            "The input rate is an illustrative assumption and is not a current provider tariff.",
            "The formula excludes setup, storage, network, energy, idle reservations, and quality variation by workload.",
        ],
    }
