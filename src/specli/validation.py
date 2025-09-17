"""
Validation utilities for specli operations.

Centralizes common validation patterns for GitHub setup, repository access,
and target path validation to reduce code duplication.
"""

from pathlib import Path
from typing import Any, Dict

from .github import ensure_github_setup, validate_repository_access


def validate_github_setup() -> Dict[str, Any]:
    """
    Validate GitHub CLI setup and authentication.

    Returns:
        Dict containing setup information with keys:
        - success: bool
        - cli_version: str
        - user_info: dict
        - message: str (for display)
    """
    try:
        setup_info = ensure_github_setup()
        return {
            "success": True,
            "setup_info": setup_info,
            "message": f"GitHub CLI v{setup_info['cli_version']} authenticated as {setup_info['user_info'].get('login', 'unknown')}",
        }
    except Exception as e:
        return {
            "success": False,
            "setup_info": None,
            "message": f"GitHub CLI error: {e}",
            "error": str(e),
        }


def validate_source_repository(repo_url: str) -> Dict[str, Any]:
    """
    Validate source repository access and existence.

    Args:
        repo_url: GitHub repository URL to validate

    Returns:
        Dict containing validation result with keys:
        - success: bool
        - repo_info: dict (if successful)
        - message: str (for display)
        - error: str (if failed)
    """
    try:
        repo_info = validate_repository_access(repo_url)
        return {
            "success": True,
            "repo_info": repo_info,
            "message": f"Source repository validated: {repo_info['full_name']}",
        }
    except Exception as e:
        return {
            "success": False,
            "repo_info": None,
            "message": f"Repository validation failed: {e}",
            "error": str(e),
        }


def validate_target_path(path: str) -> Dict[str, Any]:
    """
    Validate target path for deployment or update operations.

    Args:
        path: Target path to validate

    Returns:
        Dict containing validation result with keys:
        - success: bool
        - resolved_path: Path object (if successful)
        - message: str (for display)
        - error: str (if failed)
    """
    try:
        target_path = Path(path).resolve()

        if not target_path.exists():
            return {
                "success": False,
                "resolved_path": target_path,
                "message": f"Target path does not exist: {target_path}",
                "error": f"Path does not exist: {target_path}",
            }

        if not target_path.is_dir():
            return {
                "success": False,
                "resolved_path": target_path,
                "message": f"Target path is not a directory: {target_path}",
                "error": f"Path is not a directory: {target_path}",
            }

        return {
            "success": True,
            "resolved_path": target_path,
            "message": f"Target path validated: {target_path}",
        }
    except Exception as e:
        return {
            "success": False,
            "resolved_path": None,
            "message": f"Path validation failed: {e}",
            "error": str(e),
        }
