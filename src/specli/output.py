"""
Output formatting utilities for specli operations.

Centralizes message formatting and user feedback to ensure consistent
output across all CLI commands and operations.
"""

from pathlib import Path
from typing import Any, Dict


def format_error_message(error: str) -> str:
    """
    Format error message with consistent ERROR prefix.

    Args:
        error: Error message to format

    Returns:
        Formatted error string with "ERROR:" prefix
    """
    return f"ERROR: {error}"


def format_success_message(operation: str, details: Dict[str, Any]) -> str:
    """
    Format success message for deployment/update operations.

    Args:
        operation: Operation type ("deploy" or "update")
        details: Operation details dictionary

    Returns:
        Formatted success message string
    """
    if operation == "deploy":
        target_path = details.get("target_path", "")
        return f"Successfully deployed .claude folder to {target_path}"
    elif operation == "update":
        target_path = details.get("target_path", "")
        if details.get("fresh_deploy"):
            return f"Successfully deployed .claude folder to {target_path}"
        else:
            return f"Successfully updated .claude folder in {target_path}"
    else:
        return "Operation completed successfully"


def format_dry_run_message(action: str, target_path: str = "") -> str:
    """
    Format dry-run message with consistent DRY RUN prefix.

    Args:
        action: Action being simulated
        target_path: Optional target path for the action

    Returns:
        Formatted dry-run message string
    """
    if target_path:
        return f"   [DRY RUN] Would {action} .claude folder {'to' if 'deploy' in action else 'in'} {target_path}"
    else:
        return f"   [DRY RUN] Would {action}"


def format_operation_details(operation: str, details: Dict[str, Any]) -> list[str]:
    """
    Format operation details as a list of formatted strings.

    Args:
        operation: Operation type ("deploy" or "update")
        details: Operation details dictionary

    Returns:
        List of formatted detail strings
    """
    detail_lines = []

    if operation == "deploy" or details.get("fresh_deploy"):
        if "files_copied" in details:
            detail_lines.append(f"   Files copied: {details['files_copied']}")
        if "bytes_copied" in details:
            detail_lines.append(f"   Bytes copied: {details['bytes_copied']}")
    elif operation == "update":
        if "files_updated" in details:
            detail_lines.append(f"   Files updated: {details['files_updated']}")
        if "files_added" in details:
            detail_lines.append(f"   Files added: {details['files_added']}")
        if "files_preserved" in details:
            detail_lines.append(f"   Files preserved: {details['files_preserved']}")

    # Backup information
    if details.get("backup_created") and details.get("backup_path"):
        backup_path = Path(details["backup_path"])
        detail_lines.append(f"   Backup created: {backup_path.name}")

    return detail_lines


def format_config_message(details: Dict[str, Any], operation: str = "deploy") -> str:
    """
    Format configuration file message.

    Args:
        details: Operation details dictionary
        operation: Operation type for appropriate verb

    Returns:
        Formatted configuration message string or empty string if no config action
    """
    if details.get("config_saved") and details.get("config_file"):
        config_file = details["config_file"]
        if operation == "deploy" or details.get("fresh_deploy"):
            return f"Configuration saved: {config_file.name}"
        else:
            return f"Configuration updated: {config_file.name}"
    elif not details.get("config_saved"):
        return "Warning: Could not save/update configuration"

    return ""


def format_github_setup_message(setup_info: Dict[str, Any]) -> str:
    """
    Format GitHub CLI setup message.

    Args:
        setup_info: Setup information dictionary

    Returns:
        Formatted setup message string
    """
    cli_version = setup_info.get("cli_version", "unknown")
    user_login = setup_info.get("user_info", {}).get("login", "unknown")
    return f"GitHub CLI v{cli_version} authenticated as {user_login}"


def format_repository_validation_message(repo_info: Dict[str, Any]) -> str:
    """
    Format repository validation message.

    Args:
        repo_info: Repository information dictionary

    Returns:
        Formatted validation message string
    """
    full_name = repo_info.get("full_name", "repository")
    return f"Source repository validated: {full_name}"


def format_dry_run_config_message(config_created: bool, config_file=None) -> str:
    """
    Format dry-run configuration message.

    Args:
        config_created: Whether config creation succeeded
        config_file: Config file path object if created

    Returns:
        Formatted dry-run config message string
    """
    if config_created and config_file:
        return f"   [DRY RUN] Configuration file created: {config_file.name}"
    else:
        return "   [DRY RUN] Configuration file creation would fail"
