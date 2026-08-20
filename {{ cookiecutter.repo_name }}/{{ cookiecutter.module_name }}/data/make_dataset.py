"""Process raw data into processed Parquet.

Reads data from ``data/raw`` (CSV/JSON/Excel) and writes Parquet to
``data/processed``. Modify ``INPUT_PATH``/``OUTPUT_PATH`` or pass
alternative paths to :func:`main`.
"""

from pathlib import Path

from loguru import logger
import pandas as pd

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


def main(
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.parquet",
) -> None:
    """Process raw dataset into Parquet.

    Parameters
    ----------
    input_path : Path
        Path to raw input file (CSV by default).
    output_path : Path
        Path where processed Parquet is written.
    """
    logger.info(f"Loading raw data from {input_path}")
    # Change reader for other formats: pd.read_json / pd.read_excel / pd.read_parquet
    df = pd.read_csv(input_path)

    logger.info(f"Loaded {len(df)} rows, columns: {list(df.columns)}")

    # --- Add cleaning / transformation here ---
    # Example: df = df.dropna().reset_index(drop=True)

    logger.info(f"Saving processed data to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, compression="snappy")
    logger.success(f"Saved {len(df)} rows to {output_path}")


if __name__ == "__main__":
    main()
