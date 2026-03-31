from pathlib import Path
from typing import Any, Optional

from loguru import logger
import pickle

from {{ cookiecutter.module_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR


class BaseModel:
    """Base model class for inheritance and extension."""

    def __init__(self, params: Optional[dict[str, Any]] = None):
        """
        Initialize model.

        Parameters
        ----------
        params : dict[str, Any], optional
            Dictionary of model parameters.
        """
        self.params = params or {}
        self.model = None

    def fit(self, X, y):
        """
        Train the model.

        Parameters
        ----------
        X : array-like
            Feature data.
        y : array-like
            Target variable.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def predict(self, X):
        """
        Make predictions using the model.

        Parameters
        ----------
        X : array-like
            Feature data.

        Returns
        -------
        array-like
            Prediction results.
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call fit() first.")
        raise NotImplementedError("Subclasses must implement this method")

    def save(self, path: Path | str):
        """
        Save the model to a file.

        Parameters
        ----------
        path : Path or str
            File path to save the model.
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to: {path}")

    @classmethod
    def load(cls, path: Path | str):
        """
        Load a model from a file.

        Parameters
        ----------
        path : Path or str
            Path to the model file.

        Returns
        -------
        BaseModel
            Loaded model instance.
        """
        instance = cls()
        with open(path, "rb") as f:
            instance.model = pickle.load(f)
        logger.info(f"Model loaded from: {path}")
        return instance


def create_model(
    output_path: Path = MODELS_DIR / "model.pkl",
) -> None:
    """Create a new model instance.

    This function initializes a model and saves the default structure,
    typically used when starting a new modeling task.

    Parameters
    ----------
    output_path : Path
        Path to save the model structure.
    """
    logger.info("Creating new model...")

    model_config = {
        "name": "your_model_name",
        "version": "0.1.0",
        "hyperparameters": {},
        "created_at": None,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(model_config, f)

    logger.success(f"Model structure saved to: {output_path}")


if __name__ == "__main__":
    create_model()
