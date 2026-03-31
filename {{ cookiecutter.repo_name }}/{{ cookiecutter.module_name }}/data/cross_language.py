"""Cross-language data exchange example.

Demonstrates using Arrow/Feather format for sharing data
between Python and Julia (or other languages).
"""
import pandas as pd
from loguru import logger

from {{ cookiecutter.module_name }}.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR

# === Configuration ===
# Data to send to Julia
EXPORT_FILE = INTERIM_DATA_DIR / "for_julia.feather"

# Data received from Julia
IMPORT_FILE = INTERIM_DATA_DIR / "from_julia.feather"

# Final output
OUTPUT_FILE = PROCESSED_DATA_DIR / "final_results.parquet"

# === Export to Julia ===
logger.info("Preparing data for Julia...")

# Example: Create some data to process in Julia
df_export = pd.DataFrame(
    {"x": range(100), "y": [i**2 for i in range(100)], "category": ["A", "B"] * 50}
)

logger.info(f"Exporting to Feather: {EXPORT_FILE}")
df_export.to_feather(EXPORT_FILE)

logger.info("Data exported. Now run your Julia script to process this file.")
logger.info(
    "Julia example: using Arrow, DataFrames; df = DataFrame(Arrow.Table('for_julia.feather'))"
)

# === Import from Julia ===
# Assuming Julia has processed and saved results back
if IMPORT_FILE.exists():
    logger.info(f"Importing results from Julia: {IMPORT_FILE}")
    df_result = pd.read_feather(IMPORT_FILE)

    # Convert to Parquet for final storage
    logger.info(f"Saving final results: {OUTPUT_FILE}")
    df_result.to_parquet(OUTPUT_FILE)

    logger.success("Cross-language workflow complete.")
else:
    logger.warning(f"Julia output not found: {IMPORT_FILE}")
    logger.info("Waiting for Julia to process the data...")
