# AGENTS.md — {{ cookiecutter.project_name }} (`{{ cookiecutter.project_style }}` / `{{ cookiecutter.project_language }}`)

Shared guidance for all coding agents working in this repository.

{% if cookiecutter.project_language in ["python", "both"] %}
## Quick Start — Python{% if cookiecutter.project_language == "both" %} (hybrid){% endif %}

```bash
{% if cookiecutter.environment_manager == "uv" -%}
uv venv --python {{ cookiecutter.python_version_number }} && source .venv/bin/activate
uv sync
{% elif cookiecutter.environment_manager == "conda" -%}
conda env create -f environment.yml && conda activate {{ cookiecutter.repo_name }}
{% else -%}
# No environment manager — use your own venv
{% endif -%}
{% if cookiecutter.linting_and_formatting == "ruff" -%}
make lint          # ruff format --check && ruff check
make format        # ruff format && ruff check --fix
{% else -%}
make lint          # black --check && flake8
make format        # black + isort
{% endif -%}
```

Package management: {% if cookiecutter.environment_manager == "uv" %}always `uv add` / `uv sync` / `uv run` — never `pip`{% elif cookiecutter.environment_manager == "conda" %}`conda` + `pip` via `environment.yml`{% else %}use your preferred manager{% endif %}.
{% endif %}
{% if cookiecutter.project_language in ["julia", "both"] %}
## Quick Start — Julia{% if cookiecutter.project_language == "both" %} (hybrid){% endif %}

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
{% if cookiecutter.linting_and_formatting == "ruff" -%}
make lint-jl       # JuliaFormatter (if configured)
{% else -%}
make lint-jl       # JuliaFormatter fallback
{% endif -%}
{% if cookiecutter.project_language == "both" -%}
make lint          # runs lint-py + lint-jl
{% endif -%}
```
{% endif %}

## Programming Philosophy {% if cookiecutter.project_style == "exploratory" %}(Exploratory — script-first){% else %}(Structured — pipeline-first){% endif %}

{% if cookiecutter.project_style == "exploratory" -%}
**Default: linear script in `scripts/`.** Fast iteration over abstraction.

- Top-to-bottom execution, minimal functions/classes
- No `if __name__ == "__main__":` needed in `scripts/`
- Hardcode paths via `{{ cookiecutter.module_name }}.config` / `src/config.jl`

```python
# scripts/02_analyze.py
import pandas as pd
from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR

df = pd.read_parquet(PROCESSED_DATA_DIR / "dataset.parquet")
print(df.describe())
```

Refactor to `{{ cookiecutter.module_name }}/` only after copy-paste ×3 or need CLI/batch.
{% else -%}
**Default: layered pipeline in `{{ cookiecutter.module_name }}/` / `src/`.**

- `data/make_dataset.py` / `make_dataset.jl` — raw → processed
- `features/build_features.py` — feature engineering (`def main`)
- `models/train_model.py` — train & persist (`def main`)
- `visualization/visualize.py` — figures to `reports/figures`
- `utils/tools.py` / `utils.jl` — shared helpers only

Each module exposes `def main(input_path, output_path)` with type hints and `if __name__ == "__main__":`.

| Task | Location |
|------|----------|
| One-off exploration | `notebooks/` or `scripts/` |
| Reusable pipeline | `{{ cookiecutter.module_name }}/` |
| Repeated 3× logic | promote to `utils/` |
{% endif %}

{% if cookiecutter.project_language == "both" -%}
### Hybrid Note
- Python ↔ Julia exchange via `data/interim/*.arrow` (Arrow/Feather), not CSV/Parquet.
- Keep `data/cross_language.*` in sync: `python_to_julia.arrow` / `julia_to_python.arrow`.
{% endif %}

## Data & Storage Convention

```
data/
├── raw/        # immutable originals (any format)
├── interim/    # intermediate + cross-language (*.arrow)
├── processed/  # final analysis (ALWAYS Parquet{% if cookiecutter.project_language in ["julia","both"] %} / Arrow{% endif %})
└── external/   # third-party
reports/figures/  logs/  models/
```

- Raw may be any format; processed **always Parquet** (Python) {% if cookiecutter.project_language in ["julia","both"] %}or Arrow (Julia){% endif %}.
- By size: `<1GB pandas` / `<10GB Polars` / `>10GB DuckDB` (Python).

## Code Style Guidelines

{% if cookiecutter.project_language in ["python", "both"] -%}
### Python
- Line length 88, double quotes, import order stdlib → third-party → local
- Type hints Python 3.12 style: `list[int]`, `int | None`
- Docstring sklearn-style, raise `ValueError` with message, `loguru` + `tqdm`
{% if cookiecutter.linting_and_formatting == "ruff" -%}
- Lint/format: `ruff` (`make lint` / `make format`)
{% else -%}
- Lint/format: `flake8 + black + isort` (`make lint` / `make format`)
{% endif -%}
{% endif %}
{% if cookiecutter.project_language in ["julia", "both"] -%}
### Julia
- Use `JuliaFormatter` style, `Logging` for logs
- `include("../config.jl")` for paths in `src/`
- Mirror Python module names: `make_dataset.jl` ↔ `make_dataset.py`
{% endif %}

## Project Architecture

{% if cookiecutter.project_style == "exploratory" -%}
```
{{ cookiecutter.module_name }}/
├── config.py{% if cookiecutter.project_language in ["julia","both"] %} / src/config.jl{% endif %}
└── utils/
scripts/
├── 01_process_data.py{% if cookiecutter.project_language in ["julia","both"] %} / .jl{% endif %}
├── 02_analyze.py{% if cookiecutter.project_language in ["julia","both"] %} / .jl{% endif %}
└── 03_train_predict.py{% if cookiecutter.project_language in ["julia","both"] %} / .jl{% endif %}
```
- `scripts/` is primary — keep pipeline minimal.
{% else -%}
```
{{ cookiecutter.module_name }}/
├── config.py
├── data/make_dataset.py{% if cookiecutter.project_language == "both" %} + cross_language.py (both only){% endif %}
├── features/build_features.py
├── models/train_model.py
├── visualization/visualize.py
└── utils/tools.py
{% if cookiecutter.project_language in ["julia", "both"] -%}
src/
├── config.jl
├── data/make_dataset.jl{% if cookiecutter.project_language == "both" %} + cross_language.jl{% endif %}
├── features/build_features.jl
├── models/train_model.jl
├── visualization/visualize.jl
└── utils.jl
{% endif -%}
scripts/.gitkeep  # use for one-offs
```
{% endif %}

### Configuration
- Python: `{{ cookiecutter.module_name }}/config.py` (dotenv + loguru + tqdm)
- Julia: `src/config.jl` (mirrors Python paths)

## Skills
{% if cookiecutter.project_language in ["python", "both"] -%}
- uv package manager: `.agents/skills/uv-package-manager/SKILL.md`
{% endif -%}
{% if cookiecutter.project_language in ["julia", "both"] -%}
- Julia Pkg: `julia --project=. -e 'using Pkg; Pkg.instantiate()'` then `make lint-jl`
{% endif %}
