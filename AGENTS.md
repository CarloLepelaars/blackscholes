# AGENTS.md

Closed-form Black-Scholes-Merton, Black-76, binary options, and structures.
The published package has **no runtime dependencies**.

## Layout

```
src/blackscholes/   library (stdlib only)
  base.py           d1/d2, PDF/CDF, shared greeks
  call.py put.py    BSM, Black-76, binary
  *.py              structures (straddle, spread, …)
  mcp.py            MCP stdio server (JSON-RPC, no extra deps)
tests/test_*.py     one file per module
tests/fixtures/     example inputs and expected prices/greeks
tests/helpers.py    load cases + shared asserts
docs/               mkdocs (user-facing)
```

Public classes are re-exported from `__init__.py`. Do not re-export `mcp`.

## Conventions

- **No runtime deps.** `numpy` / `scipy` are test-only. Do not add pandas, sympy, or solvers.
- **Compact formulas.** Closed-form `math` (`exp`, `log`, `sqrt`, `erf`). Keep expressions tight.
- Shared greeks live on the base class. Type-specific ones on Call/Put.
- Structures compose legs via `_calc_attr` — never reimplement greeks.
- Params: `S, K, T, r, sigma, q=0` (BSM); `F, K, T, r, sigma` (Black-76).
- Assert `S, K, T, sigma > 0`. Use `float` throughout.
- Tests: JSON cases + put-call parity. Add a case in `tests/fixtures/*.json` to cover another market.
- Do not expand the public API or add dependencies without asking.
- MCP is stdlib JSON-RPC in `mcp.py` (`price` / `instruments`). New public classes go in `__all__` so they become kinds. Do not add the `mcp` SDK.

## Commands

```
uv sync --extra dev
uv run ruff format && uv run ruff check && uv run pytest -s
python -m blackscholes.mcp
```
