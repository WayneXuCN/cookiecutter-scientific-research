from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
# logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

# Data paths
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# Models paths
MODELS_DIR = PROJ_ROOT / "models"

# Reports paths
REPORTS_DIR = PROJ_ROOT / "reports"
LOGS_DIR = REPORTS_DIR / "logs"
FIGURES_DIR = REPORTS_DIR / "figures"

# Ensure all directories exist
for directory in [
    DATA_DIR,
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    EXTERNAL_DATA_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    LOGS_DIR,
    FIGURES_DIR,
]:
    directory.mkdir(exist_ok=True, parents=True)
# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
