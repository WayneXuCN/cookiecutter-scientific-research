from pathlib import Path

from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR


def main(
    input_path: Path = PROCESSED_DATA_DIR / "input_data.csv",
    output_path: Path = PROCESSED_DATA_DIR / "output_data.csv",
) -> None:
    """Perform tool operations on data.

    Parameters
    ----------
    input_path : Path
        Path to input data.
    output_path : Path
        Path to save output data.
    """
    logger.info("Performing tool operations...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Tool operations complete.")


if __name__ == "__main__":
    main()
