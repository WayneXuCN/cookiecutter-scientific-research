"""
Query large Parquet/Arrow files with DuckDB.
Mirrors {{ cookiecutter.module_name }}/data/large_query.py
"""

using DuckDB, DataFrames
using Logging

include("../config.jl")

const INPUT_PATTERN = joinpath(RAW_DATA_DIR, "*.parquet")
const OUTPUT_FILE = joinpath(PROCESSED_DATA_DIR, "aggregated.arrow")

@info "Querying Parquet files: $INPUT_PATTERN"

# Example using DuckDB.jl
# con = DBInterface.connect(DuckDB.DB, ":memory:")
# result = DBInterface.execute(con, \"\"\"
#     SELECT category, COUNT(*) as count, AVG(value) as mean_value
#     FROM '\$INPUT_PATTERN' GROUP BY category
# \"\"\") |> DataFrame
# Arrow.write(OUTPUT_FILE, result)

@info "Saving aggregated results to $OUTPUT_FILE"
