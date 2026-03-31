---
paths:
  - "data/**/*"
  - "**/*.parquet"
  - "**/*.feather"
  - "**/*.arrow"
---

# Data Format Guidelines

## Primary Storage: Parquet

**Use Parquet for all processed data:**

- Column-oriented, compressed, efficient for analytics
- Use for: processed datasets, model outputs, analysis results
- Tools: `pandas`, `polars`, `pyarrow`

**Raw data** can be any format (CSV, JSON, Excel). After processing, **always save as Parquet**.

## Cross-Language: Arrow/Feather

When working with Python + Julia/R:

- Use `.feather` or `.arrow` format
- Zero-copy, fast inter-process communication

## Tool Selection by Data Size

| Size | Tool | Use Case |
|------|------|----------|
| < 1 GB | pandas | Standard exploratory analysis |
| < 10 GB | Polars | Faster operations, lazy evaluation |
| > 10 GB | DuckDB | SQL queries on Parquet files |

## Storage Convention

```
data/
├── raw/        # Original data (keep original format)
├── interim/    # Intermediate (Parquet) + cross-language (Feather)
└── processed/  # Final analysis data (ALWAYS Parquet)
```
