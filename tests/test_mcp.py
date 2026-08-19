import io
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

import blackscholes as bs
from blackscholes import BlackScholesCall
from blackscholes.mcp import KINDS, _short, _version, dispatch, handle, instruments, main, price

from tests.helpers import MARKET, MARKET_2K, MARKET_3K, MARKET_CAL, MARKET_IB, MARKET_IC, almost, cases

MARKET76 = dict(F=55.0, K=50.0, T=1.0, r=0.0025, sigma=0.15)
MARKET_BIN = dict(S=55.0, K=50.0, T=1.0, r=0.0025, sigma=0.15)
SAMPLES = {
    "call": MARKET,
    "put": MARKET,
    "black76_call": MARKET76,
    "black76_put": MARKET76,
    "binary_call": MARKET_BIN,
    "binary_put": MARKET_BIN,
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


def test_kinds_cover_public_api():
    assert set(instruments()) == set(SAMPLES)
    assert set(bs.__all__) <= set(KINDS)
    for n in bs.__all__:
        assert KINDS[_short(n)] is getattr(bs, n)


@pytest.mark.parametrize("kind, params", SAMPLES.items())
def test_price_matches_class(kind, params):
    obj = KINDS[kind](**params)
    almost(price(kind, **params)["price"], obj.price())
    core = price(kind, "core", **params)
    assert core["price"] == price(kind, **params)["price"] and "delta" in core
    all_ = price(kind, "all", **params)
    assert all_["price"] == core["price"] and "delta" in all_
    almost(price(kind, "delta", **params)["delta"], obj.delta())
    almost(price(kind, "Delta", **params)["delta"], obj.delta())
    almost(price(obj.__class__.__name__, **params)["price"], obj.price())
    if kind == "call":
        almost(price(kind, "", F=None, **params)["price"], obj.price())


def test_price_errors():
    with pytest.raises(ValueError, match="Unknown kind"):
        price("nope", **MARKET)
    with pytest.raises(ValueError, match="Unknown field"):
        price("call", "not_a_greek", **MARKET)
    with pytest.raises(AssertionError):
        price("call", **{**MARKET, "S": 0})
    with pytest.raises(TypeError):
        price("call", extra=1, **MARKET)


@pytest.mark.parametrize("name, side, kind", [("bsm", "call", "call"), ("bsm", "put", "put"), ("black76", "call", "black76_call"), ("black76", "put", "black76_put"), ("binary", "call", "binary_call"), ("binary", "put", "binary_put")])
def test_fixture_prices(name, side, kind):
    for case in cases(name):
        almost(price(kind, **case["inputs"])["price"], case[side]["price"])


def _rpc(method, params=None, id=1):
    msg = {"jsonrpc": "2.0", "method": method, "id": id}
    if params is not None:
        msg["params"] = params
    return handle(msg)


def test_protocol_handshake():
    init = _rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}})
    assert init["result"]["protocolVersion"] == "2025-03-26"
    assert init["result"]["capabilities"] == {"tools": {}}
    assert init["result"]["serverInfo"]["name"] == "blackscholes"
    assert handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None
    assert _rpc("ping")["result"] == {}
    assert {t["name"] for t in _rpc("tools/list")["result"]["tools"]} == {"price", "instruments"}
    listed = _rpc("tools/call", {"name": "instruments", "arguments": {}})
    assert json.loads(listed["result"]["content"][0]["text"]) == instruments()
    want = BlackScholesCall(**MARKET).price()
    priced = _rpc("tools/call", {"name": "price", "arguments": {"kind": "call", **MARKET}})
    assert priced["result"]["isError"] is False
    almost(priced["result"]["structuredContent"]["price"], want)
    nested = _rpc("tools/call", {"name": "price", "arguments": {"kind": "call", "params": MARKET}})
    almost(nested["result"]["structuredContent"]["price"], want)
    as_str = _rpc("tools/call", {"name": "price", "arguments": {"kind": "call", "params": json.dumps(MARKET)}})
    almost(as_str["result"]["structuredContent"]["price"], want)


def test_protocol_errors():
    assert _rpc("nope")["error"]["code"] == -32601
    assert handle({"jsonrpc": "2.0", "id": 1})["error"]["code"] == -32601
    assert _rpc("initialize", {"protocolVersion": "0.0"})["result"]["protocolVersion"] == "2025-03-26"
    assert _rpc("initialize")["result"]["protocolVersion"] == "2025-03-26"
    assert _rpc("ping", [])["result"] == {}
    assert _rpc("tools/call", {"name": "price", "arguments": {"kind": "nope"}})["result"]["isError"] is True
    assert _rpc("tools/call", {"name": "nope", "arguments": {}})["result"]["isError"] is True
    assert _rpc("tools/call", {"name": "price", "arguments": {}})["result"]["isError"] is True
    for m, key in (("resources/list", "resources"), ("resources/templates/list", "resourceTemplates"), ("prompts/list", "prompts")):
        assert _rpc(m)["result"][key] == []


def test_dispatch_and_main(monkeypatch, capsys):
    dispatch("not-json")
    assert json.loads(capsys.readouterr().out)["error"]["code"] == -32700
    dispatch("1")
    assert json.loads(capsys.readouterr().out)["error"]["code"] == -32600
    dispatch(json.dumps({"jsonrpc": "2.0", "method": "ping"}))
    assert capsys.readouterr().out == ""
    dispatch(json.dumps([{"jsonrpc": "2.0", "method": "ping", "id": 1}, {"jsonrpc": "2.0", "method": "notifications/initialized"}]))
    assert json.loads(capsys.readouterr().out)[0]["result"] == {}
    dispatch(json.dumps([]))
    assert capsys.readouterr().out == ""
    dispatch(json.dumps([1]))
    assert capsys.readouterr().out == ""
    monkeypatch.setattr(sys, "stdin", io.StringIO('\n{"jsonrpc":"2.0","method":"ping","id":1}\n'))
    main()
    assert json.loads(capsys.readouterr().out)["id"] == 1
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")}
    proc = subprocess.run([sys.executable, "-m", "blackscholes.mcp"], input='{"jsonrpc":"2.0","method":"ping","id":2}\n', text=True, capture_output=True, check=True, env=env)
    assert json.loads(proc.stdout)["id"] == 2
    sys.modules.pop("blackscholes.mcp", None)
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    runpy.run_module("blackscholes.mcp", run_name="__main__")


def test_version_fallback(monkeypatch):
    import importlib.metadata as md

    monkeypatch.setattr(md, "version", lambda *_a, **_k: (_ for _ in ()).throw(md.PackageNotFoundError("blackscholes")))
    assert _version() == "0.2.4"
    monkeypatch.setattr(md, "version", lambda *_a, **_k: "9.9.9")
    assert _version() == "9.9.9"
