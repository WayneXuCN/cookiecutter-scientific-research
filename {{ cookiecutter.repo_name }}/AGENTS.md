# AGENTS.md

Shared guidance for all coding agents working in this repository.

## Quick Start

```bash
# Environment setup (uses uv, not pip)
uv venv --python 3.12
source .venv/bin/activate  # Unix/macOS
uv sync

# Code quality
make format   # ruff format && ruff check --fix
make lint     # ruff format --check && ruff check
```

**Package management:** Always use `uv add`, `uv sync`, `uv run` — never `pip`.

## Programming Style Philosophy

**This is a scientific research project.** Default to exploratory/script-based programming.

### Default: Exploratory Style

**When to use:** Most research tasks — data analysis, experiments, quick explorations.

- Linear, top-to-bottom execution in `.py` files
- Minimal abstraction: avoid unnecessary functions/classes
- No `if __name__ == "__main__":` guard needed
- No command-line argument parsing

```python
# analysis_v1.py - Quick exploration
import pandas as pd
from src.config import DATA_DIR, FIGURES_DIR

df = pd.read_parquet(DATA_DIR / "raw" / "data.parquet")
summary = df.groupby("condition").agg({"metric": ["mean", "std"]})
print(summary)
```

### When to Switch: Modular Style

**Triggers:** Same logic copy-pasted 3+ times, need CLI, building shared utilities.

| Situation | Style |
|-----------|-------|
| "Quick plot of results" | Exploratory |
| "Testing a hypothesis" | Exploratory |
| "I've written this loader 3 times" | Modular |
| "Need to run on 100 datasets" | Modular |

**Anti-pattern:** Don't over-engineer exploratory code with classes and config objects.

## Data Format and Tool Selection

### Primary Storage: Parquet

Raw data can be any format. After processing, **always save as Parquet**.

```python
df = pd.read_csv(RAW_DATA_DIR / "original.csv")
df_processed = df.dropna().reset_index(drop=True)
df_processed.to_parquet(PROCESSED_DATA_DIR / "results.parquet")
```

### Cross-Language: Arrow/Feather

For Python + Julia/R: use `.feather` or `.arrow` format.

### Tool Selection by Data Size

| Size | Tool | Use Case |
|------|------|----------|
| < 1 GB | **pandas** | Standard analysis |
| < 10 GB | **Polars** | Lazy evaluation |
| > 10 GB | **DuckDB** | SQL on Parquet |

```python
# DuckDB for large files
import duckdb
result = duckdb.sql("""
    SELECT category, AVG(value) as mean_value
    FROM 'data/raw/*.parquet'
    GROUP BY category
""").to_df()
```

### Storage Convention

```
data/
├── raw/        # Original data (any format) — keep intact
├── interim/    # Intermediate (Parquet) + cross-language (Feather)
└── processed/  # Final analysis data (ALWAYS Parquet)
```

## Code Style Guidelines

### Formatting

- **Line Length**: 88 characters
- **Quote Style**: Double quotes
- **Import Order**: stdlib → third-party → local (blank lines between)

```python
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DATA_DIR
```

### Type Hints (Python 3.12+ style)

- Built-in generics: `list[int]`, `dict[str, float]`
- Union syntax: `int | None` — avoid legacy `typing.Union`

### Documentation (sklearn-style)

```python
def compute_probability(x: float, y: float) -> float:
    """Compute joint probability from marginals.

    Parameters
    ----------
    x : float
        First marginal probability.
    y : float
        Second marginal probability.

    Returns
    -------
    float
        Joint probability value.
    """
```

### Error Handling

- Raise `ValueError` for invalid inputs with descriptive messages
- Use early returns for edge cases

### Logging

- Use `loguru` for logging, `tqdm` for progress bars

## Project Architecture

```
src/
├── config.py       # Central paths and logger
├── models/         # Model definitions
├── analyze/        # Analysis modules
└── utils/          # Shared utilities

data/
├── raw/            # Immutable original data
├── interim/        # Intermediate processing
├── processed/      # Final datasets (Parquet)
└── external/       # Third-party data

models/             # Saved model files (.pkl)
reports/figures/    # Generated plots
reports/logs/       # Experiment logs
```

### Configuration (`src/config.py`)

- Centralized path management
- Environment variable loading via `.env`
- Loguru logger with tqdm integration

## Skills

- **uv package manager:** See `.agents/skills/uv-package-manager/SKILL.md`
