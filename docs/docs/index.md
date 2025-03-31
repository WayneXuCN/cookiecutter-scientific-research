# Cookiecutter Data Science

_A logical, flexible, and reasonably standardized project structure for doing and sharing data science work._

![PyPI - Version](https://img.shields.io/pypi/v/cookiecutter-scientific-research)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookiecutter-scientific-research)
<a target="_blank" href="https://cookiecutter-scientific-research.drivendata.org/">
    <img src="https://img.shields.io/badge/ccsr-Project%20template-328F97?logo=cookiecutter" />
</a>
[![tests](https://github.com/waynexucn/cookiecutter-scientific-research/actions/workflows/tests.yml/badge.svg)](https://github.com/waynexucn/cookiecutter-scientific-research/actions/workflows/tests.yml)

!!! info "ccsr V2 Announcement"

    Version 2 of Cookiecutter Data Science has launched recently. To learn more about what's different and what's in progress, see the [announcement blog post for more information](https://drivendata.co/blog/ccsr-v2).


## Quickstart

Cookiecutter Data Science v2 requires Python 3.9+. Since this is a cross-project utility application, we recommend installing it with [pipx](https://pypa.github.io/pipx/). Installation command options:

=== "With pipx (recommended)"

    ```bash
    pipx install cookiecutter-scientific-research

    # From the parent directory where you want your project
    ccsr
    ```

=== "With pip"

    ```bash
    pip install cookiecutter-scientific-research
    `
    # From the parent directory where you want your project
    ccsr
    ```

=== "With conda (coming soon!)"

    ```bash
    # conda install cookiecutter-scientific-research -c conda-forge

    # From the parent directory where you want your project
    # ccsr
    ```

=== "Use the v1 template"

    ```bash
    pip install cookiecutter

    # From the parent directory where you want your project
    cookiecutter https://github.com/waynexucn/cookiecutter-scientific-research -c v1
    ```

!!! info "Use the ccsr command-line tool"

    Cookiecutter Data Science v2 now requires installing the new `cookiecutter-scientific-research` Python package, which extends the functionality of the [`cookiecutter`](https://cookiecutter.readthedocs.io/en/stable/README.html) templating utility. Use the provided `ccsr` command-line program instead of `cookiecutter`.


## Starting a new project

Starting a new project is as easy as running this command at the command line. No need to create a directory first, the cookiecutter will do it for you.

```bash
ccsr
```

The `ccsr` commandline tool defaults to the Cookiecutter Data Science template, but you can pass your own template as the first argument if you want.


## Example

<!-- TERMYNAL OUTPUT -->


Now that you've got your project, you're ready to go! You should do the following:

 - **Check out the directory structure** below so you know what's in the project and how to use it.
 - **Read the [opinions](opinions.md)** that are baked into the project so you understand best practices and the philosophy behind the project structure.
 - **Read the [using the template](using-the-template.md) guide** to understand how to get started on a project that uses the template.


 Enjoy!


## Directory structure

The directory structure of your new project will look something like this (depending on the settings that you choose):

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         {{ cookiecutter.module_name }} and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── {{ cookiecutter.module_name }}   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes {{ cookiecutter.module_name }} a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations   
```
