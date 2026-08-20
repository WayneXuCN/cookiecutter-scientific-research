# CLAUDE.md — {{ cookiecutter.project_name }}

<!-- Import shared agent instructions -->
@AGENTS.md

## Claude Code Specific

### Quick Commands

```bash
{% if cookiecutter.project_language in ["python", "both"] -%}
{% if cookiecutter.environment_manager == "uv" -%}
uv sync
{% elif cookiecutter.environment_manager == "conda" -%}
conda env create -f environment.yml && conda activate {{ cookiecutter.repo_name }}
{% endif -%}
{% if cookiecutter.linting_and_formatting == "ruff" -%}
make format   # ruff format && ruff check --fix
make lint     # ruff format --check && ruff check
{% else -%}
make format   # black + isort
make lint     # black --check && flake8
{% endif -%}
{% endif -%}
{% if cookiecutter.project_language in ["julia", "both"] -%}
julia --project=. -e 'using Pkg; Pkg.instantiate()'
make lint-jl
{% if cookiecutter.project_language == "both" -%}
make lint     # lint-py + lint-jl
{% endif -%}
{% endif -%}
make clean
```

### Skills

{% if cookiecutter.project_language in ["python", "both"] -%}
For uv workflows: `.claude/skills/uv-package-manager/SKILL.md`
{% endif -%}
{% if cookiecutter.project_language in ["julia", "both"] -%}
For Julia: `julia --project=. -e 'using Pkg; Pkg.instantiate()'`
{% endif %}

### Rules Organization

Detailed guidelines split into `.claude/rules/`:
{% if cookiecutter.project_language in ["python", "both"] -%}
- `python-style.md` — Python style (loads for `*.py`)
{% endif -%}
{% if cookiecutter.project_language in ["julia", "both"] -%}
- `julia-style.md` — Julia style (loads for `*.jl`)
{% endif -%}
- `data-formats.md` — Parquet/Arrow conventions (loads for `data/**/*`)
- `testing.md` — Test conventions (loads for `tests/**/*`)
{% if cookiecutter.project_style == "exploratory" -%}
- Exploratory note: prefer linear `scripts/` over new modules.
{% else -%}
- Structured note: prefer `{{ cookiecutter.module_name }}/` pipeline modules.
{% endif %}
