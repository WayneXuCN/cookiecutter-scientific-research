import json
import os
import sys
from pathlib import Path
from subprocess import run

from conftest import bake_project

BASH_EXECUTABLE = os.getenv("BASH_EXECUTABLE", "bash")


def _decode_print_stdout_stderr(result):
    """Print command stdout and stderr to console to use when debugging failing tests
    Normally hidden by pytest except in failure we want this displayed
    """
    encoding = sys.stdout.encoding

    if encoding is None:
        encoding = "utf-8"

    print("\n======================= STDOUT ======================")
    stdout = result.stdout.decode(encoding)
    print(stdout)

    print("\n======================= STDERR ======================")
    stderr = result.stderr.decode(encoding)
    print(stderr)

    return stdout, stderr


def no_curlies(filepath):
    """Utility to make sure no curly braces appear in a file.
    That is, was Jinja able to render everything?
    """
    data = filepath.open("r").read()

    template_strings = ["{{", "}}", "{%", "%}"]

    template_strings_in_file = [s in data for s in template_strings]
    return not any(template_strings_in_file)


def test_baking_configs(config, fast):
    """For every generated config in the config_generator, run all
    of the tests.
    """
    print("using config", json.dumps(config, indent=2))
    with bake_project(config) as project_directory:
        verify_folders(project_directory, config)
        verify_files(project_directory, config)

        if fast < 2:
            verify_makefile_commands(project_directory, config)


def verify_folders(root, config):
    """Tests that expected folders and only expected folders exist."""
    project_language = config.get("project_language", "python")
    project_style = config.get("project_style", "structured")

    expected_dirs = [
        ".",
        "data",
        "data/external",
        "data/interim",
        "data/processed",
        "data/raw",
        "docs",
        "models",
        "notebooks",
        "references",
        "reports",
        "reports/figures",
        "reports/logs",
        "scripts",
    ]

    # Python package dirs
    if project_language in ["python", "both"]:
        expected_dirs += [config["module_name"]]
        if config["include_code_scaffold"] == "Yes":
            if project_style == "structured":
                expected_dirs += [
                    f"{config['module_name']}/data",
                    f"{config['module_name']}/features",
                    f"{config['module_name']}/models",
                    f"{config['module_name']}/visualization",
                    f"{config['module_name']}/utils",
                ]
            else:  # exploratory - only utils remains
                expected_dirs += [
                    f"{config['module_name']}/utils",
                ]

    # Julia src dirs
    if project_language in ["julia", "both"]:
        expected_dirs += ["src"]
        if config["include_code_scaffold"] == "Yes" and project_style == "structured":
            expected_dirs += [
                "src/data",
                "src/features",
                "src/models",
                "src/visualization",
            ]
        # exploratory has no subdirs

    if config["docs"] == "mkdocs":
        expected_dirs += ["docs/docs"]

    # Tests only for python (julia tests not scaffolded)
    if (
        project_language in ["python", "both"]
        and config.get("testing_framework", "none") != "none"
    ):
        expected_dirs += ["tests"]

    # Agent guidance directories
    agent_guidance = config.get("agent_guidance", "openai")
    if agent_guidance in ("claude", "both"):
        expected_dirs += [
            ".claude",
            ".claude/rules",
            ".claude/skills",
        ]
        # uv skill only for python/both
        if project_language in ["python", "both"]:
            expected_dirs += [
                ".claude/skills/uv-package-manager",
            ]
    if agent_guidance in ("openai", "both"):
        expected_dirs += [
            ".agents",
            ".agents/rules",
            ".agents/skills",
        ]
        if project_language in ["python", "both"]:
            expected_dirs += [
                ".agents/skills/uv-package-manager",
            ]

    expected_dirs = [
        #  (root / d).resolve().relative_to(root) for d in expected_dirs
        Path(d)
        for d in expected_dirs
    ]

    existing_dirs = [
        d.resolve().relative_to(root) for d in root.glob("**") if d.is_dir()
    ]

    assert sorted(existing_dirs) == sorted(expected_dirs)


def verify_files(root, config):
    """Test that expected files and only expected files exist."""
    project_language = config.get("project_language", "python")
    project_style = config.get("project_style", "structured")

    expected_files = [
        ".gitattributes",
        "Makefile",
        "README.md",
        ".env",
        ".gitignore",
        "data/external/.gitkeep",
        "data/interim/.gitkeep",
        "data/processed/.gitkeep",
        "data/raw/.gitkeep",
        "docs/.gitkeep",
        "notebooks/.gitkeep",
        "references/.gitkeep",
        "reports/.gitkeep",
        "reports/figures/.gitkeep",
        "reports/logs/.gitkeep",
        "models/.gitkeep",
    ]

    # Scripts handling: structured or scaffold No -> only .gitkeep, exploratory+Yes -> example scripts per language
    if config["include_code_scaffold"] == "No" or project_style == "structured":
        expected_files += ["scripts/.gitkeep"]
    else:  # exploratory + Yes
        if project_language in ["python", "both"]:
            expected_files += [
                "scripts/01_process_data.py",
                "scripts/02_analyze.py",
                "scripts/03_train_predict.py",
            ]
        if project_language in ["julia", "both"]:
            expected_files += [
                "scripts/01_process_data.jl",
                "scripts/02_analyze.jl",
                "scripts/03_train_predict.jl",
            ]
        # no .gitkeep when real scripts exist

    # Python files
    if project_language in ["python", "both"]:
        expected_files += [
            "pyproject.toml",
            f"{config['module_name']}/__init__.py",
        ]
        if config["include_code_scaffold"] == "Yes":
            if project_style == "structured":
                expected_files += [
                    f"{config['module_name']}/config.py",
                    f"{config['module_name']}/data/__init__.py",
                    f"{config['module_name']}/data/make_dataset.py",
                    f"{config['module_name']}/features/__init__.py",
                    f"{config['module_name']}/features/build_features.py",
                    f"{config['module_name']}/models/__init__.py",
                    f"{config['module_name']}/models/train_model.py",
                    f"{config['module_name']}/visualization/__init__.py",
                    f"{config['module_name']}/visualization/visualize.py",
                    f"{config['module_name']}/utils/__init__.py",
                    f"{config['module_name']}/utils/tools.py",
                ]
                # cross_language only for both
                if project_language == "both":
                    expected_files += [
                        f"{config['module_name']}/data/cross_language.py",
                    ]
            else:  # exploratory - only config + utils
                expected_files += [
                    f"{config['module_name']}/config.py",
                    f"{config['module_name']}/utils/__init__.py",
                    f"{config['module_name']}/utils/tools.py",
                ]
        else:
            # include_code_scaffold No - only __init__.py (already added) - empty
            pass
        # dependency_file for python
        dep_file = config["dependency_file"]
        if dep_file != "pyproject.toml":
            expected_files.append(dep_file)

    # Julia files
    if project_language in ["julia", "both"]:
        expected_files += [
            "Project.toml",
            f"src/{config['module_name']}.jl",
        ]
        if config["include_code_scaffold"] == "Yes":
            expected_files += [
                "src/config.jl",
                "src/utils.jl",
            ]
            if project_style == "structured":
                expected_files += [
                    "src/data/make_dataset.jl",
                    "src/features/build_features.jl",
                    "src/models/train_model.jl",
                    "src/visualization/visualize.jl",
                ]
                if project_language == "both":
                    expected_files += [
                        "src/data/cross_language.jl",
                    ]
        # exploratory has no extra files beyond config/utils
        # scaffold No: only main module file

    # conditional files
    if not config["open_source_license"].startswith("No license"):
        expected_files.append("LICENSE")

    if (
        project_language in ["python", "both"]
        and config["linting_and_formatting"] == "flake8+black+isort"
    ):
        expected_files.append("setup.cfg")

    if config["docs"] == "mkdocs":
        expected_files += [
            "docs/mkdocs.yml",
            "docs/README.md",
            "docs/docs/index.md",
            "docs/docs/getting-started.md",
        ]

    if (
        project_language in ["python", "both"]
        and config.get("testing_framework", "none") != "none"
    ):
        expected_files += [
            "tests/test_data.py",
        ]

    # Agent guidance files — now only openai/claude/both, openai is default
    agent_guidance = config.get("agent_guidance", "openai")
    if agent_guidance in ("claude", "both"):
        expected_files += [
            "CLAUDE.md",
            ".claude/rules/data-formats.md",
            ".claude/rules/testing.md",
        ]
        if project_language in ["python", "both"]:
            expected_files += [".claude/rules/python-style.md"]
        if project_language in ["julia", "both"]:
            expected_files += [".claude/rules/julia-style.md"]
        if project_language in ["python", "both"]:
            expected_files += [".claude/skills/uv-package-manager/SKILL.md"]
    if agent_guidance in ("openai", "both"):
        expected_files += [
            "AGENTS.md",
            ".agents/rules/data-formats.md",
            ".agents/rules/testing.md",
        ]
        if project_language in ["python", "both"]:
            expected_files += [".agents/rules/python-style.md"]
        if project_language in ["julia", "both"]:
            expected_files += [".agents/rules/julia-style.md"]
        if project_language in ["python", "both"]:
            expected_files += [".agents/skills/uv-package-manager/SKILL.md"]

    expected_files = [Path(f) for f in expected_files]

    existing_files = [f.relative_to(root) for f in root.glob("**/*") if f.is_file()]

    assert sorted(existing_files) == sorted(set(expected_files)), (
        f"Expected {sorted(set(expected_files))} but got {sorted(existing_files)} diff: extra {sorted(set(existing_files) - set(expected_files))} missing {sorted(set(expected_files) - set(existing_files))}"
    )

    for f in existing_files:
        assert no_curlies(root / f)


def verify_makefile_commands(root, config):
    """Actually shell out to bash and run the make commands for:
    - blank command listing commands
    - create_environment
    - requirements
    - linting
    - formatting
    Ensure that these use the proper environment.
    """
    project_language = config.get("project_language", "python")
    # For julia-only, python harness not applicable - just check make help
    if project_language == "julia":
        result = run(
            [BASH_EXECUTABLE, "-c", f"cd {root.resolve()} && make help"],
            capture_output=True,
        )
        stdout_output, stderr_output = _decode_print_stdout_stderr(result)
        assert "Available rules:" in stdout_output
        assert "clean" in stdout_output
        assert result.returncode == 0
        return

    test_path = Path(__file__).parent

    if config["environment_manager"] == "conda":
        harness_path = test_path / "conda_harness.sh"
    elif config["environment_manager"] == "uv":
        harness_path = test_path / "uv_harness.sh"
    elif config["environment_manager"] == "none":
        return True
    else:
        raise ValueError(
            f"Environment manager '{config['environment_manager']}' not found in test harnesses."
        )

    result = run(
        [
            BASH_EXECUTABLE,
            str(harness_path),
            str(root.resolve()),
            str(config["module_name"]),
        ],
        capture_output=True,
    )

    stdout_output, stderr_output = _decode_print_stdout_stderr(result)

    # Check that makefile help ran successfully
    assert "Available rules:" in stdout_output
    assert "clean" in stdout_output

    # Check that linting and formatting ran successfully (only for python)
    if project_language in ["python", "both"]:
        if config["linting_and_formatting"] == "ruff":
            assert "All checks passed!" in stdout_output
            assert "left unchanged" in stdout_output
            assert "reformatted" not in stdout_output
        elif config["linting_and_formatting"] == "flake8+black+isort":
            assert "All done!" in stderr_output
            assert "left unchanged" in stderr_output
            assert "reformatted" not in stderr_output

    assert result.returncode == 0
