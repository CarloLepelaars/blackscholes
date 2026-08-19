"""Load example market cases from tests/fixtures/.

Add a case to tests/fixtures/{bsm,black76,binary}.json:

    {"id": "...", "inputs": {...}, "call": {"price": ..., "delta": ...}, "put": {...}}
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


def cases(name: str) -> list[dict]:
    return json.loads((FIXTURES / f"{name}.json").read_text())["test_cases"]


def almost(actual, expected, decimal=6, msg=""):
    np.testing.assert_almost_equal(actual, expected, decimal=decimal, err_msg=msg)


def assert_methods(obj, expected: dict, decimal: int = 6) -> None:
    for name, want in expected.items():
        got = getattr(obj, name)
        almost(got() if callable(got) else got, want, decimal, name)


def assert_option(obj, expected: dict, decimal: int = 6) -> None:
    """Check each method, plus get_core_greeks / get_all_greeks / get_itm_proxies when present."""
    assert_methods(obj, expected, decimal)
    for name in ("get_core_greeks", "get_itm_proxies", "get_all_greeks"):
        fn = getattr(obj, name, None)
        if fn is None:
            continue
        got = fn()
        assert set(got) <= set(expected), name
        for key, value in got.items():
            almost(value, expected[key], min(decimal, 5), f"{name}.{key}")


def assert_rejects(cls, valid: dict, *overrides: dict) -> None:
    for bad in overrides:
        with pytest.raises(AssertionError):
            cls(**{**valid, **bad})


def assert_positive_params(cls, valid: dict, keys: tuple[str, ...]) -> None:
    assert_rejects(cls, valid, *({k: 0.0} for k in keys), *({k: -abs(valid[k]) or -1.0} for k in keys))
    cls(**{**valid, "r": -abs(valid["r"])})


def assert_structure(structure, combo) -> None:
    leg = next(v for v in structure.__dict__.values() if hasattr(v, "get_all_greeks"))
    for attr in (*leg.get_all_greeks(), "price"):
        if attr not in ("lambda_greek", "alpha"):
            assert getattr(structure, attr)() == combo(structure, attr), attr


def assert_bsm_parity(inp: dict) -> None:
    from blackscholes import BlackScholesCall, BlackScholesPut

    c, p = BlackScholesCall(**inp), BlackScholesPut(**inp)
    q_df, r_df = exp(-inp.get("q", 0.0) * inp["T"]), exp(-inp["r"] * inp["T"])
    spot = exp((inp["r"] - inp.get("q", 0.0)) * inp["T"])
    almost(c.delta() - p.delta(), q_df, 5)
    almost(c.spot_delta() - p.spot_delta(), spot, 5)
    almost(c.dual_delta() + p.dual_delta(), r_df, 5)
    assert 0.0 < c.in_the_money() < 1.0 and 0.0 < p.in_the_money() < 1.0
    assert 0.0 < c.dual_delta() < 1.0 and 0.0 < p.dual_delta() < 1.0
    assert c.in_the_money() + p.in_the_money() == 1.0


def assert_black76_parity(inp: dict) -> None:
    from blackscholes import Black76Call, Black76Put

    c, p = Black76Call(**inp), Black76Put(**inp)
    almost(c.delta() - p.delta(), exp(-inp["r"] * inp["T"]), 5)
