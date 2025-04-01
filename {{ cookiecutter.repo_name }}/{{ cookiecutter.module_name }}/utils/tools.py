from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, MODELS_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "input_data.csv",
    output_path: Path = PROCESSED_DATA_DIR / "output_data.csv",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Performing tool operations...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Tool operations complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
