"""
Configuration file management for specli.

Handles saving and loading configuration files that store source repository
information for deployment and update operations.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def save_config(
    repository_url: str, target_path: Path, branch: Optional[str] = None
) -> Dict[str, Any]:
    """
    Save configuration file with repository information.

    Args:
        repository_url: The source repository URL
        target_path: The target directory where config should be saved
        branch: Optional branch/tag information

    Returns:
        Dictionary with operation results including 'success' status
    """
    config_file = target_path / "specli.settings.json"

    try:
        # Ensure target directory exists
        target_path.mkdir(parents=True, exist_ok=True)

        # Create configuration data
        config_data = {
            "repository_url": repository_url,
            "branch": branch,
            "deployed_at": datetime.now().replace(microsecond=0).isoformat() + "Z",
        }

        # Write configuration to file
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "config_file": config_file,
            "repository_url": repository_url,
            "branch": branch,
        }

    except (OSError, PermissionError) as e:
        return {
            "success": False,
            "error": str(e),
            "config_file": config_file,
            "repository_url": repository_url,
            "branch": branch,
        }


def load_config(target_path: Path) -> Dict[str, Any]:
    """
    Load configuration file from target directory.

    Args:
        target_path: The directory to look for config file

    Returns:
        Dictionary with configuration data
    """
    config_file = target_path / "specli.settings.json"

    try:
        if not config_file.exists():
            return {
                "repository_url": None,
                "branch": None,
                "config_exists": False,
                "config_file": config_file,
            }

        # Read and parse the configuration file
        with open(config_file, encoding="utf-8") as f:
            config_data = json.load(f)

        # Validate required fields
        required_fields = ["repository_url", "deployed_at"]
        for field in required_fields:
            if field not in config_data:
                return {
                    "repository_url": None,
                    "branch": None,
                    "config_exists": False,
                    "config_file": config_file,
                    "error": f"Missing required field: {field}",
                }

        # Return loaded configuration
        return {
            "repository_url": config_data["repository_url"],
            "branch": config_data.get("branch"),  # Optional field
            "deployed_at": config_data["deployed_at"],
            "config_exists": True,
            "config_file": config_file,
        }

    except (json.JSONDecodeError, OSError) as e:
        return {
            "repository_url": None,
            "branch": None,
            "config_exists": False,
            "config_file": config_file,
            "error": str(e),
        }
