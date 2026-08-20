---
paths:
  - "**/*.jl"
  - "src/**/*.jl"
  - "scripts/**/*.jl"
---

# Julia Code Style

## Philosophy

- Mirror Python pipeline but in Julia: `src/data/make_dataset.jl` ↔ `data/make_dataset.py`.
- Keep exploratory scripts linear (`scripts/01_*.jl`); structured modules use `function main(...)`.

## Formatting

- Use `JuliaFormatter` (`format: .JuliaFormatter.toml` if present, otherwise Blue style).
- Line length 92, 4-space indent.

## Imports & Paths

```julia
using DataFrames, CSV, Arrow
include("../config.jl")  # for src/ modules; scripts use include("../src/config.jl")
```

## Logging

- Use `Logging` (`@info`, `@warn`) — mirrors `loguru` in Python.

## Data

- Raw → Arrow/Parquet via `CSV.read` / `Arrow.write`; processed always `*.arrow`.
- Cross-language via `data/interim/*.arrow` (see `cross_language.jl`).

## Functions

- Public API: `function main(input_path::String, output_path::String)` with docstring.
- Guard: `if abspath(PROGRAM_FILE) == @__FILE__; main(); end`
