from pathlib import Path
from typing import Optional, Dict, Any

from loguru import logger
import typer
import pickle

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, MODELS_DIR

app = typer.Typer()


class BaseModel:
    """基础模型类，用于继承和扩展。"""
    
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        """
        初始化模型。
        
        Args:
            params: 模型参数字典
        """
        self.params = params or {}
        self.model = None
    
    def fit(self, X, y):
        """
        训练模型。
        
        Args:
            X: 特征数据
            y: 目标变量
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def predict(self, X):
        """
        使用模型进行预测。
        
        Args:
            X: 特征数据
        
        Returns:
            预测结果
        """
        if self.model is None:
            raise ValueError("模型尚未训练，请先调用fit方法")
        raise NotImplementedError("子类必须实现此方法")
    
    def save(self, path):
        """
        保存模型到文件。
        
        Args:
            path: 保存路径
        """
        if self.model is None:
            raise ValueError("没有模型可保存，请先训练模型")
        
        # 确保父目录存在
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"模型已保存到: {path}")
    
    @classmethod
    def load(cls, path):
        """
        从文件加载模型。
        
        Args:
            path: 模型文件路径
        
        Returns:
            加载的模型实例
        """
        instance = cls()
        with open(path, "rb") as f:
            instance.model = pickle.load(f)
        logger.info(f"模型已从 {path} 加载")
        return instance


@app.command()
def create_model(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    output_path: Path = MODELS_DIR / "model.pkl",
    # ----------------------------------------------
):
    """
    创建一个新的模型实例。
    此命令用于初始化模型并保存默认结构，通常在开始新的建模任务时使用。
    """
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("创建新模型...")
    
    # 创建一个简单的模型结构或配置
    model_config = {
        "name": "your_model_name",
        "version": "0.1.0",
        "hyperparameters": {},
        "created_at": None  # 可以在这里添加时间戳
    }
    
    # 保存模型配置或初始化模型
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(model_config, f)
    
    logger.success(f"模型初始结构已保存到: {output_path}")
    # -----------------------------------------


if __name__ == "__main__":
    app()
