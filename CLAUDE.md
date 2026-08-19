# blackscholes

See [AGENTS.md](AGENTS.md).

Python 3.10+, `uv`, `src/` layout. Zero published deps — formulas and the MCP stdio server (`python -m blackscholes.mcp`) use stdlib only.

```
uv sync --extra dev
uv run ruff format && uv run ruff check && uv run pytest -s
```
