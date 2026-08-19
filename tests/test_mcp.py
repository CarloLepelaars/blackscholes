import json

import pytest

from blackscholes import BlackScholesCall
from blackscholes.mcp import KINDS, handle, instruments, price

from tests.helpers import MARKET, MARKET_2K, MARKET_3K, MARKET_CAL, MARKET_IB, MARKET_IC, almost, cases

MARKET76 = dict(F=55.0, K=50.0, T=1.0, r=0.0025, sigma=0.15)
SAMPLES = {
    "call": MARKET,
    "put": MARKET,
    "black76_call": MARKET76,
    "black76_put": MARKET76,
    "binary_call": MARKET,
    "binary_put": MARKET,
    "straddle_long": MARKET,
    "straddle_short": MARKET,
    "strangle_long": MARKET_2K,
    "strangle_short": MARKET_2K,
    "butterfly_long": MARKET_3K,
    "butterfly_short": MARKET_3K,
    "iron_condor_long": MARKET_IC,
    "iron_condor_short": MARKET_IC,
    "iron_butterfly_long": MARKET_IB,
    "iron_butterfly_short": MARKET_IB,
    "bull_spread": MARKET_2K,
    "bear_spread": {**MARKET_2K, "K1": 50.0, "K2": 40.0},
    "calendar_call_spread": MARKET_CAL,
    "calendar_put_spread": MARKET_CAL,
}


def test_instruments_match_kinds():
    assert set(instruments()) == set(KINDS) == set(SAMPLES)
    assert instruments()["call"] == ["S", "K", "T", "r", "sigma", "q"]
    assert instruments()["black76_call"] == ["F", "K", "T", "r", "sigma"]


@pytest.mark.parametrize("kind, params", SAMPLES.items())
def test_price_matches_class(kind, params):
    opt = KINDS[kind](**params)
    got = price(kind, **params)
    almost(got["price"], opt.price())
    almost(got["delta"], opt.delta())


def test_all_greeks_and_unknown_kind():
    got = price("call", all_greeks=True, **MARKET)
    almost(got["charm"], BlackScholesCall(**MARKET).charm())
    with pytest.raises(KeyError, match="unknown kind"):
        price("nope", **MARKET)


@pytest.mark.parametrize("name, side, kind", [("bsm", "call", "call"), ("bsm", "put", "put"), ("black76", "call", "black76_call"), ("binary", "call", "binary_call")])
def test_fixture_prices(name, side, kind):
    for case in cases(name):
        almost(price(kind, **case["inputs"])["price"], case[side]["price"])


def test_handle_prices_a_call():
    assert handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    listed = handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert {t["name"] for t in listed["result"]["tools"]} == {"price", "instruments"}
    out = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "price", "arguments": {"kind": "call", **MARKET}}})
    almost(json.loads(out["result"]["content"][0]["text"])["price"], BlackScholesCall(**MARKET).price())
    bad = handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "nope", "arguments": {}}})
    assert bad["result"]["isError"]
