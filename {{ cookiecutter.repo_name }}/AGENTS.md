# AGENTS.md

This file provides guidance to coding agents working in this repository.

## Programming Style Philosophy

**This is a scientific research project.** Choose the appropriate programming style based on the task:

### Default: Exploratory / Script-based Programming

**When to use:** Most research tasks — data analysis, experiments, quick explorations, one-off analyses.

**Characteristics:**

- Linear, top-to-bottom execution in `.py` files
- Minimal abstraction: write code directly, avoid unnecessary functions/classes
- Fast iteration: prioritize getting results quickly over code reuse
- Direct variable assignments and inline logic
- No `if __name__ == "__main__":` guard needed
- No command-line argument parsing (hardcode paths, parameters inline)

**Example:**

```python
# analysis_v1.py - Quick exploration script
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.config import DATA_DIR, FIGURES_DIR

# Load data
df = pd.read_parquet(DATA_DIR / "raw" / "experiment_results.parquet")

# Quick analysis
summary = df.groupby("condition").agg({"metric": ["mean", "std"]})
print(summary)

# Plot
fig, ax = plt.subplots()
df.boxplot(column="metric", by="condition", ax=ax)
plt.savefig(FIGURES_DIR / "exploration_v1.png")
```

### When to Switch: Modular Programming

**When to use:** Only when code becomes reusable across multiple scripts, needs automation, or requires engineering rigor.

**Triggers to refactor:**

- Same logic copy-pasted across 3+ scripts
- Need command-line interface for batch processing
- Code will be used by other team members
- Building a reusable library/tool

**Characteristics:**

- Functions with type hints and docstrings
- `if __name__ == "__main__":` entry points
- Argument parsing (e.g., `typer`, `argparse`)
- Organized into modules under `src/`

### Decision Guide

| Situation | Style | Reason |
|-----------|-------|--------|
| "Let me try this analysis idea" | Exploratory | Fast iteration |
| "Quick plot of these results" | Exploratory | One-off task |
| "Testing a hypothesis" | Exploratory | Experiment |
| "I've written this loader 3 times" | Modular | Code reuse |
| "Need to run this on 100 datasets" | Modular | Automation |
| "This will be a shared utility" | Modular | Team reuse |

### Anti-patterns to Avoid

❌ **Over-engineering exploratory code:**

```python
# DON'T do this for a one-off analysis
class DataAnalyzer:
    def __init__(self, config: AnalysisConfig): ...
    def load_data(self) -> pd.DataFrame: ...
    def preprocess(self) -> pd.DataFrame: ...
    def analyze(self) -> AnalysisResult: ...

if __name__ == "__main__":
    analyzer = DataAnalyzer(load_config())
    analyzer.run()
```

✅ **Keep it simple:**

```python
# DO this instead
df = pd.read_csv("data.csv")
df_clean = df.dropna().query("value > 0")
result = df_clean.groupby("group").mean()
print(result)
```

## Data Format and Tool Selection Strategy

### Primary Storage Format: Parquet

**Use Parquet for all processed data (intermediate and final results):**

- **Why**: Column-oriented, compressed, efficient for analytics, fast I/O
- **Use for**: All processed datasets, model outputs, analysis results
- **Tools**: `pandas`, `polars`, `pyarrow`

**Note:** Raw/original data can be in any format (CSV, JSON, Excel, etc.). Once you process it, **always save as Parquet**.

```python
# Raw data can be CSV, JSON, Excel, etc.
df = pd.read_csv(RAW_DATA_DIR / "original_data.csv")
# or: pd.read_json(), pd.read_excel(), etc.

# After processing, ALWAYS save as Parquet
df_processed = df.dropna().reset_index(drop=True)
df_processed.to_parquet(PROCESSED_DATA_DIR / "results.parquet")

# Read Parquet for further analysis
df = pd.read_parquet(PROCESSED_DATA_DIR / "results.parquet")
```

### Cross-Language: Arrow/Feather

**When working with multiple languages (Python + Julia, R, etc.):**

- **Why**: Zero-copy, language-agnostic, fast inter-process communication
- **Use for**: Intermediate results shared between Python and Julia scripts
- **Format**: `.arrow` or `.feather`

```python
# Python → Julia
df.to_feather(INTERIM_DATA_DIR / "shared_data.feather")

# Julia can read this with Arrow.jl
# df = Arrow.Table("shared_data.feather") |> DataFrame
```

### Data Processing Tool Selection

Choose the right tool based on data size and complexity:

| Data Size | Tool | Use Case |
|-----------|------|----------|
| < 1 GB | **pandas** | Standard DataFrames, exploratory analysis |
| < 10 GB | **Polars** | Faster operations, lazy evaluation |
| > 10 GB | **DuckDB** | SQL queries directly on Parquet files |

#### pandas - Default for Small/Medium Data

```python
import pandas as pd

df = pd.read_parquet(DATA_DIR / "dataset.parquet")
result = df.groupby("category").agg({"value": ["mean", "std"]})
result.to_parquet(PROCESSED_DATA_DIR / "summary.parquet")
```

#### Polars - When You Need Speed

```python
import polars as pl

# Lazy evaluation for efficiency
df = pl.scan_parquet(DATA_DIR / "dataset.parquet")
result = (
    df.group_by("category")
    .agg([pl.col("value").mean(), pl.col("value").std()])
    .collect()
)
result.write_parquet(PROCESSED_DATA_DIR / "summary.parquet")
```

#### DuckDB - For Large Files / Complex SQL

```python
import duckdb

# Query Parquet directly without loading into memory
result = duckdb.sql("""
    SELECT category, 
           AVG(value) as mean_value,
           STDDEV(value) as std_value
    FROM 'data/raw/*.parquet'
    WHERE year >= 2020
    GROUP BY category
    ORDER BY mean_value DESC
""").to_df()

result.to_parquet(PROCESSED_DATA_DIR / "summary.parquet")
```

### Data Format Decision Tree

```
Loading data?
  │
  ├─ Raw/Original data?
  │   └─ Keep original format (CSV, JSON, Excel, etc.)
  │       Don't convert raw data
  │
  └─ Processing/Saving results?
      │
      ├─ Cross-language (Python + Julia)?
      │   └─ YES → Use Arrow/Feather (.feather)
      │
      ├─ CSV required for external tools?
      │   └─ YES → Export as CSV (but ALWAYS keep Parquet master)
      │
      └─ Default workflow?
          └─ ALWAYS use Parquet (.parquet) ✓
```

### Quick Reference: Data I/O Patterns

```python
# === Pattern 1: Standard pandas workflow (CSV to Parquet) ===
import pandas as pd

# Raw data in CSV
df = pd.read_csv(RAW_DATA_DIR / "input.csv")
processed = df[df["value"] > 0].reset_index(drop=True)
# Save as Parquet
processed.to_parquet(PROCESSED_DATA_DIR / "output.parquet")

# === Pattern 2: Multiple raw formats to Parquet ===
# JSON to Parquet
df_json = pd.read_json(RAW_DATA_DIR / "data.json")
df_json.to_parquet(PROCESSED_DATA_DIR / "from_json.parquet")

# Excel to Parquet
df_excel = pd.read_excel(RAW_DATA_DIR / "data.xlsx")
df_excel.to_parquet(PROCESSED_DATA_DIR / "from_excel.parquet")

# === Pattern 3: Cross-language handoff ===
# Python preprocessing (any input → Feather for Julia)
df = pd.read_csv(RAW_DATA_DIR / "input.csv")
df.to_feather(INTERIM_DATA_DIR / "for_julia.feather")

# Julia processes and saves back
result = pd.read_feather(INTERIM_DATA_DIR / "from_julia.feather")
# Save final result as Parquet
result.to_parquet(PROCESSED_DATA_DIR / "final.parquet")

# === Pattern 4: Large file SQL query ===
import duckdb

result = duckdb.sql("""
    SELECT * FROM 'data/raw/big_file.csv' 
    WHERE date >= '2024-01-01'
""").to_df()
# Save query result as Parquet
result.to_parquet(PROCESSED_DATA_DIR / "filtered.parquet")
```

### Storage Convention

```
data/
├── raw/              # Original data (any format: CSV, JSON, Excel, etc.)
│   ├── *.csv
│   ├── *.json
│   ├── *.xlsx
│   └── ...           # Keep original format intact
├── interim/          # Cross-language exchange (Feather) + intermediate processing (Parquet)
│   ├── *.feather     # For Python ↔ Julia/R exchange
│   └── *.parquet     # For intermediate processing steps
└── processed/        # Final analysis data (ALWAYS Parquet)
    └── *.parquet     # Main storage format
```

## Available Skills

### uv Package Manager

For all Python dependency management and environment tasks, consult:

- **Skill Guide**: `.agents/skills/uv-package-manager/SKILL.md`
- **Key Patterns**: Python version management (`uv python`), virtual environments (`uv venv`), dependencies (`uv add`/`uv sync`), `uv run`, lockfile workflows

## Project Quick Start

### Environment Setup

**This project uses `uv` for all Python environment and dependency management.**

```bash
# Create and activate virtual environment
uv venv --python 3.12
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate     # Windows

# Install all dependencies
uv sync
```

**Never use:** `pip`, `pip3`, `python -m pip`, or `activate` + `pip`
**Always use:** `uv add`, `uv pip`, `uv run`, `uv sync` or `uv lock`

## Common Development Commands

### Code Quality and Formatting

```bash
# Format code
make format
# or
ruff format
ruff check --fix

# Check code quality
make lint
# or
ruff format --check
ruff check

# Clean cache files
make clean
```

## Code Style Guidelines

### Formatting

- **Line Length**: 88 characters (ruff default)
- **Quote Style**: Double quotes
- **Import Style**: Standard library → third-party → local modules
- **Type Hints**: Required for public functions
- **Documentation**: Use sklearn-style docstrings for functions and classes

### Imports

```python
# Order: stdlib → third-party → local (separated by blank lines)
# Use explicit imports; avoid `from module import *`

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DATA_DIR
```

### Type Hints

- Required for all public functions, methods, and class attributes
- Use native Python 3.12+ type annotations and avoid legacy typing aliases. Guidelines:
- Prefer built-in generics: `list[int]`, `dict[str, float]`, `set[str]` (PEP 585).
- Use `|` for unions: `int | None` (PEP 604) instead of `typing.Union`.
- Only use `typing` aliases for backward compatibility or tooling that requires them.

### Documentation

Use sklearn-style docstrings for public functions and classes:

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
- Handle `None` explicitly with `| None` types

```python
def validate_node(node: str, nodes: Sequence[str]) -> None:
    if node not in nodes:
        raise ValueError(f"Node '{node}' not in network. Valid nodes: {nodes}")
```

### Data Structures

- Prefer plain dictionaries or tuples for simple, single-use data bundles
- Use `@dataclass` only when the data structure is reused across multiple scripts/modules
- Avoid over-engineering: a `dict[str, float]` is often clearer than a custom class for one-off cases

### Script Organization (Exploratory Style)

For typical research scripts, use a flat, linear structure:

```python
# experiment_01.py
"""Brief description of what this experiment explores."""
from pathlib import Path
import pandas as pd

from src.config import DATA_DIR, FIGURES_DIR

# === Configuration ===
INPUT_FILE = DATA_DIR / "raw" / "data.csv"
OUTPUT_FILE = FIGURES_DIR / "result.png"
PARAM_A = 0.5
PARAM_B = 100

# === Load Data ===
df = pd.read_csv(INPUT_FILE)

# === Process ===
result = df.query(f"value > {PARAM_A}").head(PARAM_B)

# === Output ===
print(result.describe())
result.to_csv(DATA_DIR / "processed" / "filtered.csv")
```

No need for:

- `def main():` wrapper
- `if __name__ == "__main__":`
- Argument parsing
- Class definitions (unless genuinely needed)

### Logging and Progress

- Use `loguru` for all logging operations
- Integrate with `tqdm` for progress bars in long operations
- Critical operations should log success/error states

## Project Architecture

### Directory Structure

```text
src/
├── config.py           # Central paths and logger setup
├── models/             # Model definitions
├── training/           # Training scripts and pipelines
├── analyze/            # Analysis and evaluation modules
├── visualization/      # Plotting utilities
└── utils/              # Shared utilities

data/
├── raw/                # Immutable original data
├── interim/            # Intermediate processing
├── processed/          # Final modeling datasets
└── external/           # Third-party data

models/                 # Saved model files (.pkl)
reports/
├── figures/            # Generated plots
└── logs/               # Experiment logs
```

### Configuration System (`src/config.py`)

- Centralized path management for all project directories
- Automatic directory creation for data, models, reports
- Environment variable loading via `.env` files
- Loguru logger configuration with tqdm integration

### Data Structure

- `data/raw/`: Original immutable datasets (keep in original format: CSV, JSON, Excel, etc.)
- `data/interim/`: Intermediate processing results (Parquet), cross-language exchange (Arrow/Feather)
- `data/processed/`: Final datasets for modeling (ALWAYS Parquet)
- `data/external/`: Third-party data sources
- `models/`: Trained model files (.pkl)
- `reports/figures/`: Generated visualizations
- `reports/logs/`: Experiment logs

**File format conventions:**

- **Raw data**: Keep original format (`.csv`, `.json`, `.xlsx`, etc.) — don't modify
- **Processed data**: `.parquet` — Primary storage for ALL processed data (compressed, column-oriented)
- **Cross-language**: `.feather`/`.arrow` — Data exchange between Python ↔ Julia/R
- **External output**: `.csv` — Only when required by external tools (keep Parquet as master)
