# CLAUDE.md

This file provides guidance to coding agents working in this repository.

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

### Logging and Progress

- Use `loguru` for all logging operations
- Integrate with `tqdm` for progress bars in long operations
- Critical operations should log success/error states

## Project Architecture

### Directory Structure

```text
src/
├── config.py           # Central paths and logger setup
├── models/             # Model definitions (QBN, classical BN)
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

- `data/raw/`: Original immutable datasets
- `data/interim/`: Intermediate processing results
- `data/processed/`: Final datasets for modeling
- `data/external/`: Third-party data sources
- `models/`: Trained model files (.pkl)
- `reports/figures/`: Generated visualizations
- `reports/logs/`: Experiment logs
