"""Shared utilities."""

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, create if needed.

    Parameters
    ----------
    path : Path
        Directory path to ensure.

    Returns
    -------
    Path
        The same path, guaranteed to exist.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
