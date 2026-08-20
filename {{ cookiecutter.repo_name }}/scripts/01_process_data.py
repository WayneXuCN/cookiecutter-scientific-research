"""01 - Process raw data into Parquet (exploratory, linear script)."""

from loguru import logger
import pandas as pd

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

INPUT_PATH = RAW_DATA_DIR / "dataset.csv"
OUTPUT_PATH = PROCESSED_DATA_DIR / "dataset.parquet"

logger.info(f"Loading raw data from {INPUT_PATH}")
# For demo, create dummy data if file missing
if not INPUT_PATH.exists():
    logger.warning(f"{INPUT_PATH} not found, creating dummy data for demo")
    INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"x": range(100), "y": [i**2 for i in range(100)]}).to_csv(
        INPUT_PATH, index=False
    )

df = pd.read_csv(INPUT_PATH)
logger.info(f"Loaded {len(df)} rows")

# --- Edit here: cleaning / filtering ---
# df = df.dropna()

logger.info(f"Saving to {OUTPUT_PATH}")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(OUTPUT_PATH, compression="snappy")
logger.success(f"Done. Saved {len(df)} rows to {OUTPUT_PATH}")
