"""MCP stdio server: `python -m blackscholes.mcp` or `blackscholes-mcp`."""

from __future__ import annotations

import json
import re
import sys
from inspect import signature
from typing import Any

import blackscholes as bs

_PROTOCOLS = ("2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25", "2026-07-28")
_NUMS = ("S", "F", "K", "K1", "K2", "K3", "K4", "T", "T1", "T2", "r", "sigma", "q")
_ALL = ("price", "forward", "in_the_money", "get_all_greeks", "get_core_greeks", "get_itm_proxies")
_CORE = ("price", "get_core_greeks")


def _short(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower().removeprefix("black_scholes_")


KINDS = {k: getattr(bs, n) for n in bs.__all__ for k in (_short(n), n)}


def instruments() -> dict[str, list[str]]:
    """kind → constructor param names (short names only)."""
    return {k: list(signature(c).parameters) for k, c in KINDS.items() if k[0].islower()}


def price(kind: str, fields: str = "price", **params: Any) -> dict[str, float]:
    """Closed-form price / greeks. `fields` is 'price', 'core', 'all', or comma-separated methods."""
    key = kind.strip()
    cls = KINDS.get(key) or KINDS.get(key.lower())
    if cls is None:
        raise ValueError(f"Unknown kind {kind!r}. See instruments().")
    obj = cls(**{k: float(v) for k, v in params.items() if v is not None})
    alias = (fields or "price").strip().lower() or "price"
    names = {"all": _ALL, "core": _CORE}.get(alias) or [x.strip() for x in fields.split(",") if x.strip()] or ["price"]
    out: dict[str, float] = {}
    for n in names:
        attr = n if hasattr(obj, n) else n.lower()
        fn = getattr(obj, attr, None)
        if fn is None:
            if alias in {"all", "core"}:
                continue
            raise ValueError(f"Unknown field {n!r}")
        val = fn() if callable(fn) else fn
        out.update(val if isinstance(val, dict) else {attr: val})
    return out


def _version() -> str:
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version("blackscholes")
    except PackageNotFoundError:
        return "0.2.4"


def _ok(mid, result):
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def _err(mid, code, message):
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


def _tool(name: str | None, args: dict) -> dict:
    args = dict(args or {})
    extra = args.pop("params", None)
    if isinstance(extra, str):
        extra = json.loads(extra)
    if isinstance(extra, dict):
        args = {**extra, **args}
    if name == "instruments":
        data: Any = instruments()
    elif name == "price":
        data = price(args.pop("kind"), args.pop("fields", "price"), **args)
    else:
        return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}], "isError": True}
    return {"content": [{"type": "text", "text": json.dumps(data)}], "structuredContent": data, "isError": False}


_NUM_PROP = {"type": "number"}
TOOLS = [
    {"name": "instruments", "description": "List option/structure kinds and constructor params.", "inputSchema": {"type": "object", "properties": {}}},
    {
        "name": "price",
        "description": "Closed-form price/greeks. kind from instruments(); fields='price'|'core'|'all'|method names.",
        "inputSchema": {
            "type": "object",
            "properties": {"kind": {"type": "string"}, "fields": {"type": "string", "default": "price"}, "params": {"type": "object", "additionalProperties": {"type": "number"}}, **{n: _NUM_PROP for n in _NUMS}},
            "required": ["kind"],
        },
    },
]


def handle(msg: dict) -> dict | None:
    """One JSON-RPC message → response, or None for notifications."""
    if "id" not in msg:
        return None
    mid, method, params = msg["id"], msg.get("method"), msg.get("params")
    if not isinstance(params, dict):
        params = {}
    if method == "initialize":
        proto = params.get("protocolVersion", "2025-03-26")
        proto = proto if proto in _PROTOCOLS else "2025-03-26"
        return _ok(mid, {"protocolVersion": proto, "capabilities": {"tools": {}}, "serverInfo": {"name": "blackscholes", "version": _version()}, "instructions": "Use instruments for kinds/params, then price. European options only."})
    if method == "ping":
        return _ok(mid, {})
    if method == "tools/list":
        return _ok(mid, {"tools": TOOLS})
    if method == "tools/call":
        try:
            return _ok(mid, _tool(params.get("name"), params.get("arguments") or {}))
        except Exception as e:
            return _ok(mid, {"content": [{"type": "text", "text": str(e)}], "isError": True})
    if method in {"resources/list", "resources/templates/list", "prompts/list"}:
        key = "resourceTemplates" if "templates" in method else method.split("/")[0]
        return _ok(mid, {key: []})
    return _err(mid, -32601, f"Method not found: {method}")


def _reply(obj) -> None:
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def dispatch(raw: str) -> None:
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError as e:
        _reply(_err(None, -32700, str(e)))
        return
    if isinstance(msg, list):
        out = [r for m in msg if isinstance(m, dict) and (r := handle(m))]
        if out:
            _reply(out)
        return
    if not isinstance(msg, dict):
        _reply(_err(None, -32600, "Invalid request"))
        return
    if r := handle(msg):
        _reply(r)


def main() -> None:
    for line in sys.stdin:
        if line := line.strip():
            dispatch(line)


if __name__ == "__main__":
    main()
