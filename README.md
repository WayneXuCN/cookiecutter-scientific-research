# Cookiecutter Scientific Research
> A logical, reasonably standardized but flexible project structure for doing and sharing scientific research.
## 项目简介

这是一个用于科学研究项目的 Cookiecutter 模板，旨在提供标准化的项目结构和工具配置，帮助研究人员快速搭建高质量的科学计算和数据分析环境。

### 功能特点

- 预配置的科学计算环境
- 自动化的数据处理流程
- 可重现的实验设置
- 标准化的项目文档结构
- 集成测试和质量控制工具
- 现代化的依赖管理

## 快速开始

### 安装

Cookiecutter Scientific Research 需要 Python 3.9+。本项目尚未发布至 PyPI，而是通过 GitHub Release 分发。由于这是一个跨项目实用应用程序，我们建议使用 [pipx](https://pipx.pypa.io/stable/) / [uv](https://docs.astral.sh/uv/) 进行安装。安装命令选项：安装步骤如下：

```bash
# 1. 从 GitHub Release 下载最新版本的 wheel 文件
# 下载地址: https://github.com/waynexucn/cookiecutter-scientific-research/releases

# 2. 使用 uv 安装 (推荐)
uv tool install ./cookiecutter_scientific_research.whl

# 或使用 pipx 安装 (适合全局工具)
pipx install ./cookiecutter_scientific_research.whl

```

### 创建一个新项目

要开始一个新项目，请运行：

```bash
ccrs
```

### 项目初始化

创建项目后，进入项目目录并初始化环境：

```bash
cd your-project-name
uv venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows
uv pip install -e .
```

## 项目结构

生成的项目目录结构如下：

```
├── LICENSE            <- 开源许可证（如果选择了一个）
├── Makefile           <- 包含便捷命令的 Makefile，如 `make clean`
├── README.md          <- 为项目开发者准备的 README
├── data
│   ├── external       <- 第三方数据源
│   ├── interim        <- 已转换的中间数据
│   ├── processed      <- 用于建模的最终规范数据集
│   └── raw            <- 原始、不可变的数据转储
│
├── docs               <- 默认的 mkdocs 项目（详见 www.mkdocs.org）
│
├── notebooks          <- Jupyter / Marimo notebooks。命名约定为数字（用于排序）、
│                         创建者的首字母缩写和简短的 `-` 分隔描述，例如
│                         `1.0-jqp-initial-data-exploration`
│
├── pyproject.toml     <- 项目配置文件，包含包元数据和工具配置
│
├── references         <- 数据字典、手册和所有其他解释性材料
│
├── reports            <- 生成的分析报告，如 HTML、PDF、LaTeX 等
│   ├── logs           <- 运行日志和实验记录
│   └── figures        <- 用于报告的生成图形和图表
│
└── {{ cookiecutter.module_name }}  <- 项目源代码
    │
    ├── __init__.py         <- 使 {{ cookiecutter.module_name }} 成为一个 Python 模块
    │
    ├── config.py           <- 存储有用的变量和配置
    │
    ├── dataset.py          <- 下载或生成数据的脚本
    │
    ├── analyze             <- 数据和模型分析脚本
    │   └── analysis.py     <- 分析代码
    │
    ├── models              <- 模型定义和架构
    │   └── model.py        <- 模型构建代码
    │
    ├── process             <- 数据处理脚本
    │   └── feature.py      <- 创建建模特征的代码
    │
    └── utils               <- 通用工具脚本
    │   └── tool.py         <- 创建工具函数的代码
    │
    ├── modeling            <- 运行模型脚本
    │   ├── __init__.py 
    │   ├── predict.py      <- 使用训练好的模型进行推理的代码
    │   └── train.py        <- 训练模型的代码
    │
    └── plots.py            <- 创建可视化的代码
```

## 包管理与构建

本项目使用 `flit_core` 作为构建后端，支持现代化的 Python 包管理。可以通过以下命令生成分发包（wheel 或 source distribution）：

```bash
# 确保构建依赖已安装
uv pip install --upgrade flit_core

# 生成 wheel 文件
uv run python -m flit_core.wheel

# 或生成源码分发
uv run python -m flit_core.sdist
```

构建的分发包将保存在 `dist/` 目录中。

## 致谢

本项目基于 [cookiecutter-data-science](https://github.com/drivendataorg/cookiecutter-data-science) 开发，特此感谢 DrivenData 团队提供的优秀模板和灵感。项目在原有基础上针对科学研究场景进行了定制化改进，包括工具链优化、工作流调整和文档结构优化等。

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。
