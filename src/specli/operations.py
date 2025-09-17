"""
Business operations for specli deployment and update workflows.

Contains core business logic separated from CLI concerns to enable
better testability and reusability of deployment/update operations.
"""

import tempfile
from pathlib import Path
from typing import Any, Dict

from .backup import BackupManager
from .config import save_config
from .filesystem import (
    ClaudeFolderCorruptedError,
    ClaudeFolderNotFoundError,
    copy_claude_folder,
    detect_claude_folder,
    merge_claude_folders,
)
from .github import clone_repository


def deploy_claude_commands(
    source_repo: str, target_path: Path, dry_run: bool = False
) -> Dict[str, Any]:
    """
    Deploy .claude commands from source repository to target path.

    Args:
        source_repo: GitHub repository URL containing .claude folder
        target_path: Target path for deployment (must exist)
        dry_run: If True, simulate operation without making changes

    Returns:
        Dict containing operation result with keys:
        - success: bool
        - operation: str ("deploy")
        - details: dict with operation-specific information
        - message: str (summary message)
        - error: str (if failed)
    """
    try:
        if dry_run:
            # For dry run, just validate configuration creation
            config_result = save_config(source_repo, target_path)
            return {
                "success": True,
                "operation": "deploy",
                "dry_run": True,
                "details": {
                    "source_repo": source_repo,
                    "target_path": str(target_path),
                    "config_created": config_result["success"],
                    "config_file": config_result.get("config_file"),
                },
                "message": f"Dry run: Would deploy .claude folder to {target_path}",
            }

        # Clone source repository to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            clone_result = clone_repository(source_repo, Path(temp_dir))
            source_repo_path = clone_result["repository_path"]

            # Detect .claude folder in source
            try:
                source_claude = detect_claude_folder(source_repo_path)
            except ClaudeFolderNotFoundError:
                return {
                    "success": False,
                    "operation": "deploy",
                    "details": {
                        "source_repo": source_repo,
                        "target_path": str(target_path),
                    },
                    "message": f"No .claude folder found in source repository: {source_repo}",
                    "error": f"ClaudeFolderNotFoundError: {source_repo}",
                }
            except ClaudeFolderCorruptedError as e:
                return {
                    "success": False,
                    "operation": "deploy",
                    "details": {
                        "source_repo": source_repo,
                        "target_path": str(target_path),
                    },
                    "message": f"Corrupted .claude folder in source: {e}",
                    "error": f"ClaudeFolderCorruptedError: {e}",
                }

            # Copy .claude folder to target path
            copy_result = copy_claude_folder(source_claude, target_path)

            if copy_result["success"]:
                # Save configuration file after successful deployment
                config_result = save_config(source_repo, target_path)

                return {
                    "success": True,
                    "operation": "deploy",
                    "details": {
                        "source_repo": source_repo,
                        "target_path": str(target_path),
                        "files_copied": copy_result["files_copied"],
                        "bytes_copied": copy_result["bytes_copied"],
                        "backup_created": copy_result.get("backup_created", False),
                        "backup_path": copy_result.get("backup_path"),
                        "config_saved": config_result["success"],
                        "config_file": config_result.get("config_file"),
                    },
                    "message": f"Successfully deployed .claude folder to {target_path}",
                }
            else:
                return {
                    "success": False,
                    "operation": "deploy",
                    "details": {
                        "source_repo": source_repo,
                        "target_path": str(target_path),
                    },
                    "message": f"Failed to deploy to {target_path}: {copy_result['error']}",
                    "error": copy_result["error"],
                }

    except Exception as e:
        return {
            "success": False,
            "operation": "deploy",
            "details": {"source_repo": source_repo, "target_path": str(target_path)},
            "message": f"Unexpected deployment error: {e}",
            "error": str(e),
        }


def update_claude_commands(
    target_path: Path, source_repo: str, dry_run: bool = False, no_backup: bool = False
) -> Dict[str, Any]:
    """
    Update existing .claude commands in target path.

    Args:
        target_path: Target path containing existing .claude folder
        source_repo: GitHub repository URL to pull updates from
        dry_run: If True, simulate operation without making changes
        no_backup: If True, skip backup creation

    Returns:
        Dict containing operation result with keys:
        - success: bool
        - operation: str ("update")
        - details: dict with operation-specific information
        - message: str (summary message)
        - error: str (if failed)
    """
    try:
        # Handle backup before update (if .claude folder exists)
        backup_created = False
        backup_path = None

        try:
            target_claude = detect_claude_folder(target_path)
            # .claude folder exists, handle backup
            if not dry_run:
                backup_manager = BackupManager(target_path)
                should_backup = backup_manager.should_create_backup(no_backup=no_backup)

                if should_backup:
                    backup_result = backup_manager.create_claude_backup()
                    if backup_result["success"]:
                        backup_created = True
                        backup_path = backup_result["backup_path"]
                    else:
                        return {
                            "success": False,
                            "operation": "update",
                            "details": {
                                "target_path": str(target_path),
                                "source_repo": source_repo,
                            },
                            "message": f"Backup failed: {backup_result['error']}",
                            "error": f"BackupError: {backup_result['error']}",
                        }
        except ClaudeFolderNotFoundError:
            # No .claude folder exists, no backup needed
            target_claude = None

        if dry_run:
            return {
                "success": True,
                "operation": "update",
                "dry_run": True,
                "details": {
                    "target_path": str(target_path),
                    "source_repo": source_repo,
                    "backup_would_be_created": backup_created
                    or (target_claude is not None and not no_backup),
                },
                "message": f"Dry run: Would update .claude folder in {target_path}",
            }

        # Clone source repository to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            clone_result = clone_repository(source_repo, Path(temp_dir))
            source_repo_path = clone_result["repository_path"]

            # Detect .claude folder in source
            try:
                source_claude = detect_claude_folder(source_repo_path)
            except ClaudeFolderNotFoundError:
                return {
                    "success": False,
                    "operation": "update",
                    "details": {
                        "target_path": str(target_path),
                        "source_repo": source_repo,
                    },
                    "message": f"No .claude folder found in source repository: {source_repo}",
                    "error": f"ClaudeFolderNotFoundError: {source_repo}",
                }
            except ClaudeFolderCorruptedError as e:
                return {
                    "success": False,
                    "operation": "update",
                    "details": {
                        "target_path": str(target_path),
                        "source_repo": source_repo,
                    },
                    "message": f"Corrupted .claude folder in source: {e}",
                    "error": f"ClaudeFolderCorruptedError: {e}",
                }

            # Perform update operation
            if target_claude is not None:
                # Update existing .claude folder
                merge_result = merge_claude_folders(source_claude, target_claude)

                if merge_result["success"]:
                    # Save configuration file after successful update
                    config_result = save_config(source_repo, target_path)

                    return {
                        "success": True,
                        "operation": "update",
                        "details": {
                            "target_path": str(target_path),
                            "source_repo": source_repo,
                            "files_updated": merge_result["files_updated"],
                            "files_added": merge_result["files_added"],
                            "files_preserved": merge_result["files_preserved"],
                            "backup_created": backup_created,
                            "backup_path": str(backup_path) if backup_path else None,
                            "config_saved": config_result["success"],
                            "config_file": config_result.get("config_file"),
                        },
                        "message": f"Successfully updated .claude folder in {target_path}",
                    }
                else:
                    return {
                        "success": False,
                        "operation": "update",
                        "details": {
                            "target_path": str(target_path),
                            "source_repo": source_repo,
                        },
                        "message": f"Failed to update {target_path}: {merge_result['error']}",
                        "error": merge_result["error"],
                    }
            else:
                # No existing .claude folder, do a fresh deploy
                copy_result = copy_claude_folder(source_claude, target_path)

                if copy_result["success"]:
                    # Save configuration file after successful deployment
                    config_result = save_config(source_repo, target_path)

                    return {
                        "success": True,
                        "operation": "update",
                        "details": {
                            "target_path": str(target_path),
                            "source_repo": source_repo,
                            "files_copied": copy_result["files_copied"],
                            "bytes_copied": copy_result["bytes_copied"],
                            "fresh_deploy": True,
                            "config_saved": config_result["success"],
                            "config_file": config_result.get("config_file"),
                        },
                        "message": f"Successfully deployed .claude folder to {target_path}",
                    }
                else:
                    return {
                        "success": False,
                        "operation": "update",
                        "details": {
                            "target_path": str(target_path),
                            "source_repo": source_repo,
                        },
                        "message": f"Failed to deploy to {target_path}: {copy_result['error']}",
                        "error": copy_result["error"],
                    }

    except Exception as e:
        return {
            "success": False,
            "operation": "update",
            "details": {"target_path": str(target_path), "source_repo": source_repo},
            "message": f"Unexpected update error: {e}",
            "error": str(e),
        }
