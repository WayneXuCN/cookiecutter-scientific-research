---
paths:
  - "**/*.py"
  - "notebooks/**/*.ipynb"
---

# Python Code Style

## Programming Style Philosophy

**This is a scientific research project.** Choose the appropriate programming style based on the task.

### Default: Exploratory / Script-based Programming

**When to use:** Most research tasks — data analysis, experiments, quick explorations, one-off analyses.

- Linear, top-to-bottom execution in `.py` files
- Minimal abstraction: write code directly, avoid unnecessary functions/classes
- Fast iteration: prioritize getting results quickly over code reuse
- No `if __name__ == "__main__":` guard needed
- No command-line argument parsing (hardcode paths, parameters inline)

### When to Switch: Modular Programming

**Triggers to refactor:**

- Same logic copy-pasted across 3+ scripts
- Need command-line interface for batch processing
- Code will be used by other team members
- Building a reusable library/tool

## Formatting Rules

- **Line Length**: 88 characters (ruff default)
- **Quote Style**: Double quotes
- **Import Order**: stdlib → third-party → local (blank lines between)
- **Type Hints**: Required for public functions (Python 3.12+ style)
- **Docstrings**: sklearn-style for public functions/classes

## Import Pattern

```python
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DATA_DIR
```

## Type Hints

- Use built-in generics: `list[int]`, `dict[str, float]` (PEP 585)
- Use `|` for unions: `int | None` (PEP 604)
- Avoid legacy `typing.Union`, `typing.List`

## Error Handling

- Raise `ValueError` for invalid inputs with descriptive messages
- Use early returns for edge cases
- Handle `None` explicitly with `| None` types

## Data Structures

- Prefer plain dictionaries or tuples for simple, single-use data
- Use `@dataclass` only when reused across multiple scripts/modules
