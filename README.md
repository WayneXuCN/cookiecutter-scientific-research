### 1. **重新打包项目**

项目使用 `flit_core` 作为构建后端，可以通过以下命令生成分发包（wheel 或 sdist）：

```bash
uv pip install --upgrade flit_core  # 确保构建依赖已安装
uv run python -m flit_core.wheel  # 生成 wheel 文件
```

或生成源码分发：

```bash
uv run python -m flit_core.sdist
```

生成的包会默认输出到 `dist/` 目录。

### 注意事项

• 如果需要在生产环境安装，建议使用 `--no-editable` 标志避免可编辑模式依赖：

  ```bash
  uv pip install --no-editable ./dist/*.whl
  ```

• 若遇到依赖冲突，可通过 `uv sync --no-editable` 重新同步环境。
