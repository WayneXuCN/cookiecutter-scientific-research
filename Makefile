.PHONY: _prep create_environment requirements format lint docs docs-serve test \
	test-fastest test-debug-fastest _clean_manual_test manual-test manual-test-debug

## GLOBALS

PROJECT_NAME = cookiecutter-scientific-research
PYTHON_VERSION = 3.12
PYTHON_INTERPRETER = python


###     UTILITIES
_prep:
	rm -f **/*/.DS_store


###     DEV COMMANDS

## Set up python interpreter environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> uv venv created. Activate with:\nsource .venv/bin/activate"

## Install Python Dependencies
requirements:
	uv sync --all-extras

## Format the code using ruff
format:
	ruff check --fix ccsr hooks tests
	ruff format ccsr hooks tests

lint:
	ruff format --check ccsr hooks tests
	ruff check ccsr hooks tests

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

dist: clean ## builds source and wheel package
	python -m build
	ls -l dist


###     DOCS

docs:
	cd docs && mkdocs build

docs-serve:
	cd docs && mkdocs serve

###     TESTS

test: _prep
	pytest -vvv --durations=0 tests

test-fastest: _prep
	pytest -vvv -FFF

test-debug-last:
	pytest --lf --pdb

_clean_manual_test:
	rm -rf manual_test

manual-test: _prep _clean_manual_test
	mkdir -p manual_test
	cd manual_test && python -m ccsr ..

manual-test-debug: _prep _clean_manual_test
	mkdir -p manual_test
	cd manual_test && python -m pdb ../ccsr/__main__.py ..
