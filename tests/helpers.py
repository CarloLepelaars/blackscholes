"""Shared test helpers and JSON fixture loader.

Add a case by appending to `tests/fixtures/{bsm,black76,binary}.json`:

    {"id": "...", "inputs": {...}, "call": {"outputs": {...}}, "put": {...}}
"""

from __future__ import annotations

import json
from math import exp
from pathlib import Path

import numpy as np
import pytest

FIXTURES = Path(__file__).parent / "fixtures"

MARKET = dict(S=55.0, K=50.0, T=1.0, r=0.0025, sigma=0.15)
MARKET_2K = dict(S=55.0, K1=40.0, K2=50.0, T=1.0, r=0.0025, sigma=0.15)
MARKET_3K = dict(S=55.0, K1=40.0, K2=50.0, K3=60.0, T=1.0, r=0.0025, sigma=0.15)
MARKET_IB = dict(S=25.0, K1=20.0, K2=25.0, K3=30.0, T=1.0, r=0.0025, sigma=0.15)
MARKET_IC = dict(S=55.0, K1=20.0, K2=25.0, K3=45.0, K4=50.0, T=1.0, r=0.0025, sigma=0.15)
MARKET_CAL = dict(S=55.0, K1=40.0, K2=50.0, T1=1.0, T2=0.5, r=0.0025, sigma=0.15)

_EXCLUDE_STRUCTURE = ("lambda_greek", "alpha")


def cases(name: str) -> list[dict]:
    return json.loads((FIXTURES / f"{name}.json").read_text())["test_cases"]


def assert_almost_dict(actual: dict, expected: dict, decimal: int = 5) -> None:
    assert set(actual) == set(expected)
    for key, value in expected.items():
        np.testing.assert_almost_equal(actual[key], value, decimal=decimal, err_msg=key)


def assert_outputs(obj, outputs: dict, decimal: int = 6) -> None:
    for attr, expected in outputs.items():
        np.testing.assert_almost_equal(getattr(obj, attr)(), expected, decimal=decimal, err_msg=attr)


def assert_rejects(cls, valid: dict, *overrides: dict) -> None:
    for bad in overrides:
        with pytest.raises(AssertionError):
            cls(**{**valid, **bad})


def assert_positive_params(cls, valid: dict, keys: tuple[str, ...]) -> None:
    for key in keys:
        assert_rejects(cls, valid, {key: 0.0}, {key: -abs(valid[key]) or -1.0})
    cls(**{**valid, "r": -abs(valid["r"])})


def structure_methods(structure) -> list[str]:
    leg = next(v for v in structure.__dict__.values() if hasattr(v, "get_all_greeks"))
    return [m for m in list(leg.get_all_greeks()) + ["price"] if m not in _EXCLUDE_STRUCTURE]


def assert_structure(structure, expected) -> None:
    for attr in structure_methods(structure):
        assert getattr(structure, attr)() == expected(structure, attr), attr


def discount_q(inputs: dict) -> float:
    return exp(-inputs.get("q", 0.0) * inputs["T"])


def discount_r(inputs: dict) -> float:
    return exp(-inputs["r"] * inputs["T"])


def spot_delta_factor(inputs: dict) -> float:
    return exp((inputs["r"] - inputs.get("q", 0.0)) * inputs["T"])
