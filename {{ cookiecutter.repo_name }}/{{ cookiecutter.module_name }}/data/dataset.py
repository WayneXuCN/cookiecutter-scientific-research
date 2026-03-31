from pathlib import Path

from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


def main(
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
) -> None:
    """Process dataset from raw to processed format.

    Parameters
    ----------
    input_path : Path
        Path to input dataset.
    output_path : Path
        Path to save processed dataset.
    """
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")


if __name__ == "__main__":
    main()
