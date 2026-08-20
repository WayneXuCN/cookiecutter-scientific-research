"""Generate visualizations from processed data."""

from pathlib import Path

from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR


def main(
    input_path: Path = PROCESSED_DATA_DIR / "dataset.parquet",
    output_path: Path = FIGURES_DIR / "plot.png",
) -> None:
    """Create a simple plot from processed data.

    Parameters
    ----------
    input_path : Path
        Path to processed dataset (Parquet).
    output_path : Path
        Path where figure is saved.
    """
    logger.info(f"Loading data from {input_path}")
    df = pd.read_parquet(input_path)
    logger.info(f"Data shape: {df.shape}")

    # --- Plotting ---
    # Replace with publication-ready plotting code.
    fig, ax = plt.subplots(figsize=(6, 4))
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        df[numeric_cols[0]].hist(ax=ax, bins=30)
        ax.set_xlabel(numeric_cols[0])
        ax.set_ylabel("Count")
        ax.set_title("Distribution")
    else:
        ax.text(0.5, 0.5, "No numeric columns", ha="center")
        ax.set_axis_off()
    fig.tight_layout()

    logger.info(f"Saving figure to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.success(f"Figure saved to {output_path}")


if __name__ == "__main__":
    main()
