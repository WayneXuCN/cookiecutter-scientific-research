from pathlib import Path

from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR


def main(
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
) -> None:
    """Train a model using features and labels.

    Parameters
    ----------
    features_path : Path
        Path to features dataset.
    labels_path : Path
        Path to labels dataset.
    model_path : Path
        Path to save trained model.
    """
    logger.info("Training some model...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Modeling training complete.")


if __name__ == "__main__":
    main()
