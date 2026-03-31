"""Perform analysis on processed dataset.

Example exploratory script for data analysis.
Modify paths directly in this file.
"""
from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR

# === Configuration ===
INPUT_PATH = PROCESSED_DATA_DIR / "dataset.csv"
OUTPUT_PATH = PROCESSED_DATA_DIR / "analysis_results.csv"

# === Analysis ===
logger.info("Analyzing dataset...")

for i in tqdm(range(10), total=10):
    if i == 5:
        logger.info("Something happened for iteration 5.")

logger.success("Analysis complete.")
