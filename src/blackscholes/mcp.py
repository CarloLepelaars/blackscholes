"""MCP adapter for chat hosts that cannot import Python.

Python users should use the classes. This file is a thin stdio wrapper
around them: `python -m blackscholes.mcp`.
"""

import sys
from inspect import signature
from json import dumps, loads

from blackscholes import (
    BinaryCall,
    BinaryPut,
    Black76Call,
    Black76Put,
    BlackScholesBearSpread,
    BlackScholesBullSpread,
    BlackScholesButterflyLong,
    BlackScholesButterflyShort,
    BlackScholesCalendarCallSpread,
    BlackScholesCalendarPutSpread,
    BlackScholesCall,
    BlackScholesIronButterflyLong,
    BlackScholesIronButterflyShort,
    BlackScholesIronCondorLong,
    BlackScholesIronCondorShort,
    BlackScholesPut,
    BlackScholesStraddleLong,
    BlackScholesStraddleShort,
    BlackScholesStrangleLong,
    BlackScholesStrangleShort,
)

KINDS = {
    "call": BlackScholesCall,
    "put": BlackScholesPut,
    "black76_call": Black76Call,
    "black76_put": Black76Put,
    "binary_call": BinaryCall,
    "binary_put": BinaryPut,
    "straddle_long": BlackScholesStraddleLong,
    "straddle_short": BlackScholesStraddleShort,
    "strangle_long": BlackScholesStrangleLong,
    "strangle_short": BlackScholesStrangleShort,
    "butterfly_long": BlackScholesButterflyLong,
    "butterfly_short": BlackScholesButterflyShort,
    "iron_condor_long": BlackScholesIronCondorLong,
    "iron_condor_short": BlackScholesIronCondorShort,
    "iron_butterfly_long": BlackScholesIronButterflyLong,
    "iron_butterfly_short": BlackScholesIronButterflyShort,
    "bull_spread": BlackScholesBullSpread,
    "bear_spread": BlackScholesBearSpread,
    "calendar_call_spread": BlackScholesCalendarCallSpread,
    "calendar_put_spread": BlackScholesCalendarPutSpread,
}


def instruments():
    """kind → constructor params."""
    return {k: list(signature(cls).parameters) for k, cls in KINDS.items()}


def price(kind, all_greeks=False, **params):
    """Fair value and greeks. Same numbers as `KINDS[kind](**params)`."""
    if kind not in KINDS:
        raise KeyError(f"unknown kind {kind!r}. Choose from: {', '.join(KINDS)}")
    opt = KINDS[kind](**{k: v for k, v in params.items() if v is not None})
    greeks = opt.get_all_greeks() if all_greeks and hasattr(opt, "get_all_greeks") else opt.get_core_greeks()
    return {"price": opt.price(), **greeks}


_NUM = {"type": "number"}
TOOLS = [
    {"name": "instruments", "description": "List kinds and constructor params.", "inputSchema": {"type": "object", "properties": {}}},
    {
        "name": "price",
        "description": "Price and greeks for a European option or structure. kind from instruments().",
        "inputSchema": {
            "type": "object",
            "required": ["kind"],
            "properties": {
                "kind": {"type": "string"},
                "all_greeks": {"type": "boolean", "default": False},
                **{n: _NUM for n in "S F K K1 K2 K3 K4 T T1 T2 r sigma q".split()},
            },
        },
    },
]


def handle(msg):
    """One JSON-RPC message. Notifications (no id) return None."""
    if "id" not in msg:
        return None
    mid, method, params = msg["id"], msg.get("method"), msg.get("params") or {}
    if method == "initialize":
        result = {
            "protocolVersion": params.get("protocolVersion", "2025-03-26"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "blackscholes", "version": "0.2.4"},
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        name, args = params.get("name"), params.get("arguments") or {}
        try:
            if name == "instruments":
                data = instruments()
            elif name == "price":
                data = price(**args)
            else:
                raise ValueError(f"unknown tool: {name}")
            result = {"content": [{"type": "text", "text": dumps(data)}]}
        except Exception as e:
            result = {"content": [{"type": "text", "text": str(e)}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": str(method)}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle(loads(line))
        if out:
            print(dumps(out), flush=True)


if __name__ == "__main__":
    main()
