# AGENTS.md

This file provides guidance to coding agents working in this repository.

## Development Environment Setup

### Python Environment

- **Python Version**: 3.12+
- **Package Manager**: Use `uv` for dependency management
- **Virtual Environment**: Run `make create_environment` or `uv venv --python 3.12`

### Installing Dependencies

```bash
# Sync all dependencies
uv sync

# Install new packages
uv add package_name

# Activate environment (if not already active)
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate     # Windows
```

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

### Running Code

```bash
# Run modules directly
uv run src/training/train.py
uv run src/data/dataset.py

# Alternative method
uv run -m src.training.train
uv run -m src.data.dataset
```

### Data Processing

```bash
# Generate datasets
make data
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

### Data Structures

- Use `@dataclass` for simple data containers
- Use `field(init=False)` for computed attributes
- Prefer immutable types where possible

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
