"""
Business logic operations for specli.

This module contains the core business logic extracted from CLI commands,
enabling independent testing without CLI dependencies.
"""

import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

from .config import save_config
from .filesystem import (
    ClaudeFolderCorruptedError,
    ClaudeFolderNotFoundError,
    copy_claude_folder,
    detect_claude_folder,
    merge_claude_folders,
)
from .github import (
    GitHubCLIError,
    clone_repository,
    ensure_github_setup,
    validate_repository_access,
)


def deploy_operation(
    source_repo: str,
    target_path: Path,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Execute deploy business logic.

    Args:
        source_repo: Source repository URL
        target_path: Target path for deployment
        dry_run: Whether to perform a dry run

    Returns:
        Dictionary with success status and detailed results
    """
    result = {
        "success": False,
        "message": "",
        "dry_run": dry_run,
        "github_setup": {},
        "repository_validation": {},
        "claude_folder_found": False,
        "files_copied": 0,
        "bytes_copied": 0,
        "config_saved": False,
        "error": None,
        "errors": []
    }

    try:
        # Convert path to absolute path
        target_path = Path(target_path).resolve()

        # Handle dry run early return for config only
        if dry_run:
            config_result = save_config(source_repo, target_path)
            result["config_saved"] = config_result.get("success", False)
            result["success"] = True
            result["message"] = f"Dry run completed for {target_path}"
            return result

        # Validate GitHub setup
        try:
            setup_info = ensure_github_setup()
            result["github_setup"] = {
                "cli_version": setup_info.get("cli_version", "unknown"),
                "user_info": setup_info.get("user_info", {})
            }
        except GitHubCLIError as e:
            result["error"] = f"GitHub CLI error: {e}"
            result["errors"].append(str(e))
            return result

        # Validate source repository
        try:
            source_info = validate_repository_access(source_repo)
            result["repository_validation"] = {
                "full_name": source_info.get("full_name", "unknown")
            }
        except Exception as e:
            result["error"] = f"Repository validation error: {e}"
            result["errors"].append(str(e))
            return result

        # Clone source repository to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                clone_result = clone_repository(source_repo, Path(temp_dir))
                source_repo_path = clone_result["repository_path"]
            except Exception as e:
                result["error"] = f"Repository clone error: {e}"
                result["errors"].append(str(e))
                return result

            # Detect .claude folder in source
            try:
                source_claude = detect_claude_folder(source_repo_path)
                result["claude_folder_found"] = True
            except ClaudeFolderNotFoundError:
                result["error"] = f"No .claude folder found in source repository: {source_repo}"
                result["errors"].append(result["error"])
                return result
            except ClaudeFolderCorruptedError as e:
                result["error"] = f"Corrupted .claude folder in source: {e}"
                result["errors"].append(str(e))
                return result

            # Copy .claude folder to target path
            try:
                copy_result = copy_claude_folder(source_claude, target_path)

                if copy_result["success"]:
                    result["files_copied"] = copy_result.get("files_copied", 0)
                    result["bytes_copied"] = copy_result.get("bytes_copied", 0)

                    # Save configuration file after successful deployment
                    config_result = save_config(source_repo, target_path)
                    result["config_saved"] = config_result.get("success", False)

                    result["success"] = True
                    result["message"] = f"Successfully deployed .claude folder to {target_path}"
                else:
                    result["error"] = f"Failed to deploy to {target_path}: {copy_result.get('error', 'Unknown error')}"
                    result["errors"].append(result["error"])

            except Exception as e:
                result["error"] = f"File operation error: {e}"
                result["errors"].append(str(e))

    except Exception as e:
        result["error"] = f"Unexpected error: {e}"
        result["errors"].append(str(e))

    return result


def update_operation(
    target_path: Path,
    source_repo: Optional[str] = None,
    dry_run: bool = False,
    no_backup: bool = False
) -> Dict[str, Any]:
    """
    Execute update business logic.

    Args:
        target_path: Target path to update
        source_repo: Source repository URL (optional)
        dry_run: Whether to perform a dry run
        no_backup: Whether to skip backup creation

    Returns:
        Dictionary with success status and detailed results
    """
    result = {
        "success": False,
        "message": "",
        "dry_run": dry_run,
        "path_validation": {},
        "config_loaded": False,
        "source_from_config": None,
        "backup_needed": False,
        "backup_created": False,
        "github_setup": {},
        "repository_validation": {},
        "claude_folder_found": False,
        "files_updated": 0,
        "files_added": 0,
        "files_preserved": 0,
        "config_saved": False,
        "error": None,
        "errors": []
    }

    try:
        # Convert path to absolute path
        target_path = Path(target_path).resolve()

        # Validate target path
        result["path_validation"] = {
            "path_exists": target_path.exists(),
            "is_directory": target_path.is_dir() if target_path.exists() else False
        }

        if not result["path_validation"]["path_exists"]:
            result["error"] = f"Target path does not exist: {target_path}"
            result["errors"].append(result["error"])
            return result

        if not result["path_validation"]["is_directory"]:
            result["error"] = f"Target path is not a directory: {target_path}"
            result["errors"].append(result["error"])
            return result

        # Handle source repository selection
        if not source_repo:
            from .config import load_config
            config = load_config(target_path)
            result["config_loaded"] = config.get("config_exists", False)
            if config.get("config_exists") and config.get("repository_url"):
                source_repo = config["repository_url"]
                result["source_from_config"] = source_repo
            else:
                result["error"] = "No source repository specified and no configuration found"
                result["errors"].append(result["error"])
                return result

        # Handle backup before update (if .claude folder exists)
        try:
            target_claude = detect_claude_folder(target_path)
            result["backup_needed"] = True

            # Handle backup logic
            if not no_backup and not dry_run:
                from .backup import BackupManager
                backup_manager = BackupManager(target_path)
                should_backup = backup_manager.should_create_backup(no_backup=no_backup)

                if should_backup:
                    backup_result = backup_manager.create_claude_backup()
                    result["backup_created"] = backup_result.get("success", False)
                    if not result["backup_created"]:
                        result["error"] = f"Backup failed: {backup_result.get('error', 'Unknown error')}"
                        result["errors"].append(result["error"])
                        return result

        except ClaudeFolderNotFoundError:
            # No .claude folder exists, no backup needed
            result["backup_needed"] = False

        # Handle dry run early return
        if dry_run:
            result["success"] = True
            result["message"] = f"Dry run completed for {target_path}"
            return result

        # Validate GitHub setup
        try:
            setup_info = ensure_github_setup()
            result["github_setup"] = {
                "cli_version": setup_info.get("cli_version", "unknown"),
                "user_info": setup_info.get("user_info", {})
            }
        except GitHubCLIError as e:
            result["error"] = f"GitHub CLI error: {e}"
            result["errors"].append(str(e))
            return result

        # Validate source repository
        try:
            source_info = validate_repository_access(source_repo)
            result["repository_validation"] = {
                "full_name": source_info.get("full_name", "unknown")
            }
        except Exception as e:
            result["error"] = f"Repository validation error: {e}"
            result["errors"].append(str(e))
            return result

        # Clone source repository to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                clone_result = clone_repository(source_repo, Path(temp_dir))
                source_repo_path = clone_result["repository_path"]
            except Exception as e:
                result["error"] = f"Repository clone error: {e}"
                result["errors"].append(str(e))
                return result

            # Detect .claude folder in source
            try:
                source_claude = detect_claude_folder(source_repo_path)
                result["claude_folder_found"] = True
            except ClaudeFolderNotFoundError:
                result["error"] = f"No .claude folder found in source repository: {source_repo}"
                result["errors"].append(result["error"])
                return result
            except ClaudeFolderCorruptedError as e:
                result["error"] = f"Corrupted .claude folder in source: {e}"
                result["errors"].append(str(e))
                return result

            # Perform update operation
            try:
                # Check if target has .claude folder for merging
                try:
                    target_claude = detect_claude_folder(target_path)
                    # Merge/update .claude folders
                    merge_result = merge_claude_folders(source_claude, target_claude)

                    if merge_result["success"]:
                        result["files_updated"] = merge_result.get("files_updated", 0)
                        result["files_added"] = merge_result.get("files_added", 0)
                        result["files_preserved"] = merge_result.get("files_preserved", 0)

                        # Save configuration file after successful update
                        config_result = save_config(source_repo, target_path)
                        result["config_saved"] = config_result.get("success", False)

                        result["success"] = True
                        result["message"] = f"Successfully updated .claude folder in {target_path}"
                    else:
                        result["error"] = f"Failed to update {target_path}: {merge_result.get('error', 'Unknown error')}"
                        result["errors"].append(result["error"])

                except ClaudeFolderNotFoundError:
                    # No existing .claude folder, do a fresh deploy
                    copy_result = copy_claude_folder(source_claude, target_path)

                    if copy_result["success"]:
                        result["files_added"] = copy_result.get("files_copied", 0)
                        result["files_updated"] = 0
                        result["files_preserved"] = 0

                        # Save configuration file after successful deployment
                        config_result = save_config(source_repo, target_path)
                        result["config_saved"] = config_result.get("success", False)

                        result["success"] = True
                        result["message"] = f"Successfully deployed .claude folder to {target_path}"
                    else:
                        result["error"] = f"Failed to deploy to {target_path}: {copy_result.get('error', 'Unknown error')}"
                        result["errors"].append(result["error"])

            except Exception as e:
                result["error"] = f"Update operation error: {e}"
                result["errors"].append(str(e))

    except Exception as e:
        result["error"] = f"Unexpected error: {e}"
        result["errors"].append(str(e))

    return result