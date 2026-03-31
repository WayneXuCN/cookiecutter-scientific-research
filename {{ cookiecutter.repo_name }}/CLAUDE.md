# CLAUDE.md

<!-- Import shared agent instructions -->
@AGENTS.md

## Claude Code Specific

### Quick Commands

```bash
# Environment setup
uv sync

# Code quality
make format   # or: ruff format && ruff check --fix
make lint     # or: ruff format --check && ruff check

# Clean up
make clean
```

### Skills

For uv package manager workflows, see `.claude/skills/uv-package-manager/SKILL.md`

### Rules Organization

Detailed guidelines are split into `.claude/rules/`:

- `python-style.md` — Code style, type hints, imports (loads for `*.py` files)
- `data-formats.md` — Parquet, Feather, tool selection (loads for `data/**/*`)
- `testing.md` — Test conventions (loads for `tests/**/*`)
