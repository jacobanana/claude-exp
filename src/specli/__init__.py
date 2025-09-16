"""
specli - Claude Command Deployer

A CLI tool for deploying and synchronizing .claude commands across repositories.
"""

import tomllib
from pathlib import Path

DEFAULT_VERSION = "unknown"


def _get_version():
    """Get version from pyproject.toml file."""
    try:
        # Get the project root directory (where pyproject.toml is located)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"

        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                return data.get("project", {}).get("version", DEFAULT_VERSION)
        else:
            return DEFAULT_VERSION
    except Exception:
        return DEFAULT_VERSION


__version__ = _get_version()
