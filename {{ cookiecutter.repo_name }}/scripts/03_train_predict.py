"""03 - Train a quick model (exploratory, linear script)."""

import pickle

from loguru import logger
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from {{ cookiecutter.module_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR

FEATURES_PATH = PROCESSED_DATA_DIR / "dataset.parquet"
MODEL_PATH = MODELS_DIR / "model.pkl"

logger.info(f"Loading features from {FEATURES_PATH}")
df = pd.read_parquet(FEATURES_PATH)

# Demo: last column as label if not provided separately
if df.shape[1] >= 2:
    X = df.iloc[:, :-1].select_dtypes(include="number").fillna(0)
    y = df.iloc[:, -1]
else:
    logger.warning("Not enough columns, using dummy target")
    X = df.select_dtypes(include="number").fillna(0)
    y = pd.Series([0, 1] * (len(df) // 2) + [0] * (len(df) % 2))

logger.info(f"Training on X={X.shape}, y={y.shape}")
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

logger.info(f"Saving model to {MODEL_PATH}")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)
logger.success(f"Model saved to {MODEL_PATH}")

# Quick sanity prediction
preds = model.predict(X.head())
logger.info(f"Sample predictions: {preds[:5]}")
