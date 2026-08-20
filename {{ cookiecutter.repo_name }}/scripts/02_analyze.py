"""02 - Exploratory analysis (linear script, no functions)."""

from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR

INPUT_PATH = PROCESSED_DATA_DIR / "dataset.parquet"

logger.info(f"Loading processed data from {INPUT_PATH}")
df = pd.read_parquet(INPUT_PATH)
logger.info(f"Shape: {df.shape}\n{df.describe()}")

# --- Quick analysis ---
numeric_cols = df.select_dtypes(include="number").columns.tolist()
logger.info(f"Numeric columns: {numeric_cols}")
if numeric_cols:
    summary = df[numeric_cols].agg(["mean", "std", "min", "max"])
    logger.info(f"Summary:\n{summary}")

# --- Quick plot ---
fig, ax = plt.subplots(figsize=(6, 4))
if numeric_cols:
    df[numeric_cols[0]].hist(ax=ax, bins=30)
    ax.set_xlabel(numeric_cols[0])
    ax.set_ylabel("Count")
    ax.set_title("Exploratory histogram")
else:
    ax.text(0.5, 0.5, "No numeric data", ha="center")
    ax.set_axis_off()
fig.tight_layout()
out = FIGURES_DIR / "02_analyze_hist.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, bbox_inches="tight")
logger.success(f"Figure saved to {out}")
