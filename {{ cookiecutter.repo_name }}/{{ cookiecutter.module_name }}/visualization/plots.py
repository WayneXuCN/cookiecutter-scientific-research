from pathlib import Path

from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR


def main(
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
) -> None:
    """Generate visualization plots from processed data.

    Parameters
    ----------
    input_path : Path
        Path to input data.
    output_path : Path
        Path to save generated plot.
    """
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")


if __name__ == "__main__":
    main()
