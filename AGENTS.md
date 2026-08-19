# AGENTS.md

Closed-form Black-Scholes-Merton, Black-76, binary options, and structures.
The published package has **no runtime dependencies**.

## Layout

```
src/blackscholes/   library (stdlib only)
  base.py           d1/d2, PDF/CDF, shared greeks
  call.py put.py    BSM, Black-76, binary
  *.py              structures (straddle, spread, …)
tests/test_*.py     one file per module
docs/               mkdocs (user-facing)
```

Public classes are re-exported from `__init__.py`.

## Conventions

- **No runtime deps.** `numpy` / `scipy` are test-only. Do not add pandas, sympy, or solvers.
- **Compact formulas.** Closed-form `math` (`exp`, `log`, `sqrt`, `erf`). Keep expressions tight.
- Shared greeks live on the base class. Type-specific ones on Call/Put.
- Structures compose legs via `_calc_attr` — never reimplement greeks.
- Params: `S, K, T, r, sigma, q=0` (BSM); `F, K, T, r, sigma` (Black-76).
- Assert `S, K, T, sigma > 0`. Use `float` throughout.
- Tests: golden values + put-call parity. `np.testing.assert_almost_equal`.
- Do not expand the public API or add dependencies without asking.

## Commands

```
uv sync --extra dev
uv run ruff format && uv run ruff check && uv run pytest -s
```
