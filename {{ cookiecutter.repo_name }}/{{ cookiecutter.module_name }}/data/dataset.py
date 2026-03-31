"""Process dataset from raw to processed format.

Example script for data preprocessing.
Reads original data (CSV/JSON/Excel) and saves as Parquet.
"""
import pandas as pd
from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

# === Configuration ===
# Raw data can be in any format
INPUT_FILE = RAW_DATA_DIR / "dataset.csv"  # or .json, .xlsx, etc.
OUTPUT_FILE = PROCESSED_DATA_DIR / "dataset.parquet"  # ALWAYS Parquet

# === Load Data ===
logger.info(f"Loading raw data from {INPUT_FILE}")

# Read from original format
df = pd.read_csv(INPUT_FILE)
# Or: pd.read_json(), pd.read_excel(), pd.read_parquet(), etc.

# === Processing ===
logger.info("Processing dataset...")

# Example: Filter and transform
# Modify this section for your actual processing logic
for i in tqdm(range(10), total=10):
    if i == 5:
        logger.info("Something happened for iteration 5.")

# === Save Results ===
logger.info(f"Saving processed data to {OUTPUT_FILE}")
# Always save processed data as Parquet
df.to_parquet(OUTPUT_FILE, compression="snappy")

logger.success(f"Processing complete. Saved to Parquet format.")
