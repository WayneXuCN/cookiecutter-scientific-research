"""Perform inference using a trained model.

Example exploratory script for model prediction.
Modify paths directly in this file.
"""
from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR

# === Configuration ===
FEATURES_PATH = PROCESSED_DATA_DIR / "test_features.csv"
MODEL_PATH = MODELS_DIR / "model.pkl"
PREDICTIONS_PATH = PROCESSED_DATA_DIR / "test_predictions.csv"

# === Inference ===
logger.info("Performing inference for model...")

for i in tqdm(range(10), total=10):
    if i == 5:
        logger.info("Something happened for iteration 5.")

logger.success("Inference complete.")
