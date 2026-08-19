#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_VERSION = {{ cookiecutter.python_version_number }}
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Clean all files cache
.PHONY: clean
clean:
{% if cookiecutter.project_language in ["python", "both"] %}
	@echo "Delete compiled Python files..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
{% endif %}
{% if cookiecutter.project_language in ["julia", "both"] %}
	@echo "Cleaning Julia cache..."
	find . -type d -name "*.jl.cov" -delete 2>/dev/null || true
{% endif %}
{% if cookiecutter.notebook == 'jupyterlab' %}
	@echo "Cleaning Jupyter Notebooks cache..."
	find . -name "*.ipynb" -exec jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {} \; 2>/dev/null || true
{% endif %}
{% if cookiecutter.notebook == 'marimo' %}
	@echo "Cleaning Marimo cache..."
	find . -type d -name "__marimo__" -exec rm -rf {} + 2>/dev/null || true
{% endif %}
{% if cookiecutter.project_language in ["python", "both"] and cookiecutter.linting_and_formatting == 'ruff' %}
	@echo "Cleaning ruff cache..."
	ruff clean
{% endif %}

{% if cookiecutter.project_language in ["python", "both"] %}
{% if cookiecutter.linting_and_formatting == 'ruff' %}
## Lint using ruff (use `make format` to do formatting)
.PHONY: lint lint-py
lint: lint-py
lint-py:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format format-py
format: format-py
format-py:
	ruff check --fix
	ruff format
{% elif cookiecutter.linting_and_formatting == 'flake8+black+isort' %}
## Lint using flake8, black, and isort (use `make format` to do formatting)
.PHONY: lint lint-py
lint: lint-py
lint-py:
	flake8 {{ cookiecutter.module_name }}
	isort --check --diff {{ cookiecutter.module_name }}
	black --check {{ cookiecutter.module_name }}

## Format source code with black
.PHONY: format format-py
format: format-py
format-py:
	isort {{ cookiecutter.module_name }}
	black {{ cookiecutter.module_name }}
{% endif %}
{% endif %}
{% if cookiecutter.project_language in ["julia", "both"] %}
## Lint Julia code (placeholder - configure JuliaFormatter if needed)
.PHONY: lint-jl
lint-jl:
	@echo "Julia lint: configure JuliaFormatter.jl for formatting checks"

## Format Julia code (placeholder)
.PHONY: format-jl
format-jl:
	@echo "Julia format: run 'julia -e \"using JuliaFormatter; format(\".\")\"' after adding JuliaFormatter"
{% endif %}

{% if cookiecutter.project_language in ["python", "both"] and cookiecutter.testing_framework != 'none' %}
## Run tests
.PHONY: test test-py
test: test-py
test-py:
{%- if cookiecutter.testing_framework == 'unittest' %}
	python -m unittest discover -s tests
{%- elif cookiecutter.testing_framework == 'pytest' %}
	python -m pytest tests
{%- endif -%}
{%- endif -%}
{% if cookiecutter.project_language in ["julia", "both"] %}
## Run Julia tests
.PHONY: test-jl
test-jl:
	julia --project=. -e 'using Pkg; Pkg.test()'
{% endif %}

{% if not cookiecutter.dataset_storage.none %}
## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
	{% if cookiecutter.dataset_storage.s3 -%}
	aws s3 sync s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/ \
		data/ {% if cookiecutter.dataset_storage.s3.aws_profile != 'default' %} --profile {{ cookiecutter.dataset_storage.s3.aws_profile }}{% endif %}
	{% elif cookiecutter.dataset_storage.azure -%}
	az storage blob download-batch -s {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-d data/
	{% elif cookiecutter.dataset_storage.gcs -%}
	gsutil -m rsync -r gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/ data/
	{% endif %}

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
	{% if cookiecutter.dataset_storage.s3 -%}
	aws s3 sync data/ \
		s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data {% if cookiecutter.dataset_storage.s3.aws_profile != 'default' %} --profile {{ cookiecutter.dataset_storage.s3.aws_profile }}{% endif %}
	{% elif cookiecutter.dataset_storage.azure -%}
	az storage blob upload-batch -d {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-s data/
	{% elif cookiecutter.dataset_storage.gcs -%}
	gsutil -m rsync -r data/ gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/
	{% endif %}
{% endif %}

{% if cookiecutter.project_language in ["python", "both"] and cookiecutter.environment_manager != 'none' %}
## Set up Python interpreter environment
.PHONY: create_environment create_environment-py
create_environment: create_environment-py
create_environment-py:
	{% if cookiecutter.environment_manager == 'conda' -%}
	{% if cookiecutter.dependency_file != 'environment.yml' %}
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	{% else -%}
	conda env create --name $(PROJECT_NAME) -f environment.yml
	{% endif %}
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'uv' -%}
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
{% endif %}
{% endif %}
{% if cookiecutter.project_language in ["python", "both"] %}
## Install dependencies
.PHONY: requirements requirements-py
requirements: requirements-py
requirements-py:
	{% if cookiecutter.environment_manager == 'uv' -%}
	uv sync
	{% elif cookiecutter.environment_manager == 'conda' -%}
	@echo "Conda environment dependencies via environment.yml"
	{% else -%}
	pip install -e .
	{% endif %}
{% endif %}
{% if cookiecutter.project_language in ["julia", "both"] %}
## Set up Julia environment
.PHONY: create_environment-jl
create_environment-jl:
	julia --project=. -e 'using Pkg; Pkg.instantiate()'
	@echo ">>> Julia environment instantiated. Activate with: julia --project=."
{% endif %}

{% if cookiecutter.project_language == "julia" %}
## Generic aliases for Julia-only (so `make lint` etc. work)
.PHONY: lint
lint: lint-jl
.PHONY: format
format: format-jl
.PHONY: test
test: test-jl
.PHONY: data
data: data-jl
.PHONY: create_environment
create_environment: create_environment-jl
{% elif cookiecutter.project_language == "both" %}
## Generic aliases for both languages
.PHONY: lint
lint: lint-py lint-jl
.PHONY: format
format: format-py format-jl
.PHONY: test
test: test-py test-jl
.PHONY: data
data: data-py data-jl
.PHONY: create_environment
create_environment: create_environment-py create_environment-jl
{% endif %}


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

{% if cookiecutter.include_code_scaffold == 'Yes' %}
{% if cookiecutter.project_language in ["python", "both"] %}
## Make dataset with Python
.PHONY: data data-py
data: data-py
data-py: requirements
	$(PYTHON_INTERPRETER) {{ cookiecutter.module_name }}/data/dataset.py
{% endif %}
{% if cookiecutter.project_language in ["julia", "both"] %}
## Make dataset with Julia
.PHONY: data-jl
data-jl:
	julia --project=. src/data/dataset.jl
{% endif %}
{% endif %}
{% if cookiecutter.project_style == 'exploratory' %}
{% if cookiecutter.project_language in ["python", "both"] %}
## Run exploratory Python scripts
.PHONY: run-py
run-py:
	@echo "Run exploratory Python scripts: uv run python scripts/*.py"
{% endif %}
{% if cookiecutter.project_language in ["julia", "both"] %}
## Run exploratory Julia scripts
.PHONY: run-jl
run-jl:
	@echo "Run exploratory Julia scripts: julia --project=. scripts/*.jl"
{% endif %}
{% endif %}

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST) 2>/dev/null || python3 -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST) 2>/dev/null || grep -E "^##" $(MAKEFILE_LIST) | sed 's/^## //'
