"""Build features from processed dataset."""

from pathlib import Path

from loguru import logger
import pandas as pd
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR


def main(
    input_path: Path = PROCESSED_DATA_DIR / "dataset.parquet",
    output_path: Path = PROCESSED_DATA_DIR / "features.parquet",
) -> None:
    """Generate features from processed data and save as Parquet.

    Parameters
    ----------
    input_path : Path
        Path to processed dataset (Parquet).
    output_path : Path
        Path where feature table is written (Parquet).
    """
    logger.info(f"Loading processed data from {input_path}")
    df = pd.read_parquet(input_path)
    logger.info(f"Input shape: {df.shape}")

    # --- Feature engineering ---
    # Replace with domain-specific transforms. Example placeholder:
    logger.info("Building features...")
    for _ in tqdm(range(1), desc="features"):
        # Example: df["feat_mean"] = df.select_dtypes("number").mean(axis=1)
        pass

    logger.info(f"Saving features to {output_path} (shape={df.shape})")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, compression="snappy")
    logger.success("Feature building complete.")


if __name__ == "__main__":
    main()
