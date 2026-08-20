"""Train and persist a model from feature table."""

from pathlib import Path

from loguru import logger
import pandas as pd

from {{ cookiecutter.module_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR

try:
    from sklearn.ensemble import RandomForestClassifier

    _HAS_SKLEARN = True
except ImportError:
    _HAS_SKLEARN = False


def main(
    features_path: Path = PROCESSED_DATA_DIR / "features.parquet",
    labels_path: Path | None = None,
    model_path: Path = MODELS_DIR / "model.pkl",
) -> None:
    """Train a model and save to ``model_path``.

    Parameters
    ----------
    features_path : Path
        Path to feature table (Parquet). If ``labels_path`` is ``None``,
        the last column is treated as label for the demo.
    labels_path : Path | None
        Optional separate label file.
    model_path : Path
        Where to persist the trained model (pickle).
    """
    import pickle

    logger.info(f"Loading features from {features_path}")
    df = pd.read_parquet(features_path)

    if labels_path is not None:
        y = pd.read_parquet(labels_path).squeeze("columns")
        X = df
    elif df.shape[1] >= 2:
        # Demo heuristic: last column is label
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        logger.warning("No labels_path given; using last column as label (demo).")
    else:
        logger.warning("Not enough columns for train/label split; using dummy data.")
        X = df
        y = pd.Series([0] * len(df))

    logger.info(f"Training model on X={X.shape}, y={y.shape}")
    if _HAS_SKLEARN and len(X) > 5:
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X.select_dtypes(include="number").fillna(0), y)
    else:
        # Fallback dummy model for tiny / no-sklearn environments
        class DummyModel:
            def predict(self, X):  # type: ignore[no-untyped-def]
                import numpy as np

                return np.zeros(len(X), dtype=int)

        model = DummyModel()
        logger.warning("Using DummyModel (install scikit-learn or provide more rows).")

    logger.info(f"Saving model to {model_path}")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logger.success(f"Model saved to {model_path}")


if __name__ == "__main__":
    main()
