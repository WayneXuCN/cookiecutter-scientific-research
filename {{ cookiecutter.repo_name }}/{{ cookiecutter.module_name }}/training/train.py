"""Train a model using features and labels.

Example exploratory script for model training.
Modify paths and parameters directly in this file.
"""
from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR

# === Configuration ===
FEATURES_PATH = PROCESSED_DATA_DIR / "features.csv"
LABELS_PATH = PROCESSED_DATA_DIR / "labels.csv"
MODEL_PATH = MODELS_DIR / "model.pkl"

# === Training ===
logger.info("Training some model...")

for i in tqdm(range(10), total=10):
    if i == 5:
        logger.info("Something happened for iteration 5.")

logger.success("Modeling training complete.")
