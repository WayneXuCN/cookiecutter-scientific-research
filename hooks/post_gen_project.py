import shutil
import uuid
from copy import copy
from pathlib import Path

# https://github.com/cookiecutter/cookiecutter/issues/824
#   our workaround is to include these utility functions in the ccsr package
from ccsr.hook_utils.custom_config import write_custom_config
from ccsr.hook_utils.dependencies import (
    basic,
    flake8_black_isort,
    jupyterlab,
    marimo,
    packages,
    ruff,
    scaffold,
    write_dependencies,
    write_python_version,
)

#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#
packages_to_install = copy(packages)

# {% if cookiecutter.dataset_storage.s3 %}
packages_to_install += ["awscli"]
# {% endif %} #

# {% if cookiecutter.include_code_scaffold == "Yes" %}
packages_to_install += scaffold
# {% endif %}

# {% if cookiecutter.pydata_packages == "basic" %}
packages_to_install += basic
# {% endif %}

# {% if cookiecutter.notebook == "marimo" %}
packages_to_install += marimo
# {% endif %}

# {% if cookiecutter.notebook == "jupyterlab" %}
packages_to_install += jupyterlab
# {% endif %}

# {% if cookiecutter.linting_and_formatting == "ruff" %}
packages_to_install += ruff
# Remove setup.cfg
Path("setup.cfg").unlink()
# {% elif cookiecutter.linting_and_formatting == "flake8+black+isort" %}
packages_to_install += flake8_black_isort
# {% endif %}
# track packages that are not available through conda
pip_only_packages = [
    "awscli",
    "python-dotenv",
]

# Select testing framework
tests_path = Path("tests")

# {% if cookiecutter.testing_framework == "pytest" %}
packages_to_install += ["pytest"]
# {% endif %}

# {% if cookiecutter.testing_framework == "none" %}
shutil.rmtree(tests_path)

# {% else %}
tests_subpath = tests_path / "{{ cookiecutter.testing_framework }}"
for obj in tests_subpath.iterdir():
    shutil.move(str(obj), str(tests_path))

# Remove all remaining tests templates
for tests_template in tests_path.iterdir():
    if tests_template.is_dir() and not tests_template.name == "tests":
        shutil.rmtree(tests_template)
# {% endif %}

# Use the selected documentation package specified in the config,
# or none if none selected
docs_path = Path("docs")
# {% if cookiecutter.docs != "none" %}
packages_to_install += ["{{ cookiecutter.docs }}"]
pip_only_packages += ["{{ cookiecutter.docs }}"]
docs_subpath = docs_path / "{{ cookiecutter.docs }}"
for obj in docs_subpath.iterdir():
    shutil.move(str(obj), str(docs_path))
# {% endif %}

# Remove all remaining docs templates
for docs_template in docs_path.iterdir():
    if docs_template.is_dir() and not docs_template.name == "docs":
        shutil.rmtree(docs_template)

#
#  Handle project_language (python / julia / both)
#
project_language = "{{ cookiecutter.project_language }}"
project_style = "{{ cookiecutter.project_style }}"

# Python-only: remove Julia artifacts
if project_language == "python":
    julia_src = Path("src")
    if julia_src.exists():
        shutil.rmtree(julia_src)
    proj_toml = Path("Project.toml")
    if proj_toml.exists():
        proj_toml.unlink()
    # Remove Julia scripts if any (keep scripts dir for python)
    # No extra cleanup needed

# Julia-only: remove Python artifacts
elif project_language == "julia":
    py_pkg = Path("{{ cookiecutter.module_name }}")
    if py_pkg.exists():
        shutil.rmtree(py_pkg)
    for py_file in [
        "pyproject.toml",
        "requirements.txt",
        "environment.yml",
        "setup.cfg",
    ]:
        p = Path(py_file)
        if p.exists():
            p.unlink()
    # Remove Python tests (no Julia test scaffold yet)
    if tests_path.exists():
        shutil.rmtree(tests_path)
    # Remove Python-specific dependency artifacts - skip write_dependencies below
    packages_to_install = []  # no python deps to write

# Both: keep everything, nothing to delete for language

#
#  Handle project_style == exploratory (lightweight)
#
if project_style == "exploratory":
    # Python exploratory: keep only config.py and utils/, plus __init__.py
    if project_language in ["python", "both"]:
        py_pkg = Path("{{ cookiecutter.module_name }}")
        if py_pkg.exists():
            for child in list(py_pkg.iterdir()):
                if child.is_dir() and child.name not in ["utils"]:
                    shutil.rmtree(child)
                elif child.is_file() and child.name not in ["__init__.py", "config.py"]:
                    child.unlink()
            init_py = py_pkg / "__init__.py"
            if init_py.exists():
                pass
    # Julia exploratory: keep only config.jl, utils.jl, and main module file
    if project_language in ["julia", "both"]:
        julia_src = Path("src")
        if julia_src.exists():
            for child in list(julia_src.iterdir()):
                if child.is_dir():
                    shutil.rmtree(child)
                elif child.is_file() and child.name not in [
                    "config.jl",
                    "utils.jl",
                    "{{ cookiecutter.module_name }}.jl",
                ]:
                    child.unlink()
    # Ensure scripts directory exists for exploratory (once)
    Path("scripts").mkdir(exist_ok=True)
    if not any(Path("scripts").iterdir()):
        (Path("scripts") / ".gitkeep").write_text("")

# Structured keeps full scaffold - no trimming needed
# But include_code_scaffold == "No" still applies after this (below)

# Generate unique UUID for Julia Project.toml
if Path("Project.toml").exists():
    try:
        _proj_text = Path("Project.toml").read_text()
        if "00000000-0000-0000-0000-000000000001" in _proj_text:
            _proj_text = _proj_text.replace(
                "00000000-0000-0000-0000-000000000001", str(uuid.uuid4())
            )
            Path("Project.toml").write_text(_proj_text)
    except Exception:
        pass

#
#  POST-GENERATION FUNCTIONS
#
# Only write Python dependencies if python is part of the project
if project_language in ["python", "both"]:
    write_dependencies(
        "{{ cookiecutter.dependency_file }}",
        packages_to_install,
        pip_only_packages,
        repo_name="{{ cookiecutter.repo_name }}",
        module_name="{{ cookiecutter.module_name }}",
        python_version="{{ cookiecutter.python_version_number }}",
    )
    write_python_version("{{ cookiecutter.python_version_number }}")
else:
    # For julia-only, dependency_file may be pyproject.toml which we deleted; nothing to do
    pass

write_custom_config("{{ cookiecutter.custom_config }}")

# Remove LICENSE if "No license file"
if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink()

agent_guidance = "{{ cookiecutter.agent_guidance }}"
claude_file = Path("CLAUDE.md")
agents_file = Path("AGENTS.md")
claude_dir = Path(".claude")
agents_dir = Path(".agents")

if agent_guidance == "none":
    if claude_file.exists():
        claude_file.unlink()
    if agents_file.exists():
        agents_file.unlink()
    if claude_dir.exists():
        shutil.rmtree(claude_dir)
    if agents_dir.exists():
        shutil.rmtree(agents_dir)
elif agent_guidance == "claude":
    if agents_file.exists():
        agents_file.unlink()
    if agents_dir.exists():
        shutil.rmtree(agents_dir)
elif agent_guidance == "openai":
    if claude_file.exists():
        claude_file.unlink()
    if claude_dir.exists():
        shutil.rmtree(claude_dir)

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
if Path("pyproject.toml").exists():
    pyproject_text = Path("pyproject.toml").read_text()
    Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))

# {% if cookiecutter.include_code_scaffold == "No" %}
# remove everything except __init__.py so result is an empty package
if project_language in ["python", "both"]:
    py_pkg_path = Path("{{ cookiecutter.module_name }}")
    if py_pkg_path.exists():
        for generated_path in list(py_pkg_path.iterdir()):
            if generated_path.is_dir():
                shutil.rmtree(generated_path)
            elif generated_path.name != "__init__.py":
                generated_path.unlink()
            elif generated_path.name == "__init__.py":
                generated_path.write_text("")
if project_language in ["julia", "both"]:
    julia_src_path = Path("src")
    if julia_src_path.exists():
        for generated_path in list(julia_src_path.iterdir()):
            if generated_path.is_dir():
                shutil.rmtree(generated_path)
            elif generated_path.name not in ["{{ cookiecutter.module_name }}.jl"]:
                generated_path.unlink()
            elif generated_path.name == "{{ cookiecutter.module_name }}.jl":
                generated_path.write_text(
                    "module {{ cookiecutter.module_name }}\nend\n"
                )
# {% endif %}
