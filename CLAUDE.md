# blackscholes

See [AGENTS.md](AGENTS.md).

Python 3.10+, `uv`, `src/` layout. Zero published deps — formulas use stdlib `math`. MCP (`python -m blackscholes.mcp`) is a thin stdio adapter, also stdlib.

```
uv sync --extra dev
uv run ruff format && uv run ruff check && uv run pytest -s
```
