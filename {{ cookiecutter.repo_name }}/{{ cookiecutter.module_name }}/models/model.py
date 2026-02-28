from pathlib import Path
from typing import Optional, Dict, Any

from loguru import logger
import typer
import pickle

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, MODELS_DIR

app = typer.Typer()


class BaseModel:
    """Base model class for inheritance and extension."""
    
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        """
        Initialize model.
        
        Args:
            params: Dictionary of model parameters
        """
        self.params = params or {}
        self.model = None
    
    def fit(self, X, y):
        """
        Train the model.
        
        Args:
            X: Feature data
            y: Target variable
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def predict(self, X):
        """
        Make predictions using the model.
        
        Args:
            X: Feature data
        
        Returns:
            Prediction results
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call fit() first.")
        raise NotImplementedError("Subclasses must implement this method")
    
    def save(self, path):
        """
        Save the model to a file.
        
        Args:
            path: File path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to: {path}")
    
    @classmethod
    def load(cls, path):
        """
        Load a model from a file.
        
        Args:
            path: Path to the model file
        
        Returns:
            Loaded model instance
        """
        instance = cls()
        with open(path, "rb") as f:
            instance.model = pickle.load(f)
        logger.info(f"Model loaded from: {path}")
        return instance


@app.command()
def create_model(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    output_path: Path = MODELS_DIR / "model.pkl",
    # ----------------------------------------------
):
    """
    Create a new model instance.
    This command initializes a model and saves the default structure,
    typically used when starting a new modeling task.
    """
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
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
    # -----------------------------------------


if __name__ == "__main__":
    app()
