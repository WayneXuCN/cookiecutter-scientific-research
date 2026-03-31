"""Query large Parquet files with DuckDB.

Example script for processing large datasets using SQL.
DuckDB can query Parquet files directly without loading into memory.
"""
import duckdb
from loguru import logger

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

# === Configuration ===
INPUT_PATTERN = RAW_DATA_DIR / "*.parquet"  # Wildcard pattern
OUTPUT_FILE = PROCESSED_DATA_DIR / "aggregated.parquet"

# === SQL Query on Parquet ===
logger.info(f"Querying Parquet files: {INPUT_PATTERN}")

query = f"""
    SELECT 
        category,
        COUNT(*) as count,
        AVG(value) as mean_value,
        STDDEV(value) as std_value
    FROM '{INPUT_PATTERN}'
    WHERE value > 0
    GROUP BY category
    ORDER BY mean_value DESC
"""

result = duckdb.sql(query).to_df()

# === Save Results ===
logger.info(f"Saving aggregated results to {OUTPUT_FILE}")
result.to_parquet(OUTPUT_FILE)

logger.success(f"Processed {len(result)} categories.")
