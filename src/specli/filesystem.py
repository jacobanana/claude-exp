"""
File system operations for .claude folder management.

This module handles:
- Detection of .claude folders in repositories
- Copying .claude folders between repositories
- Updating existing .claude folders with merge logic
- Backup creation and restoration
- File system error handling
"""

import os
import shutil
import time
from pathlib import Path
from typing import Optional, Dict, List, Tuple


class ClaudeFolderNotFoundError(Exception):
    """Raised when .claude folder is not found in source repository."""
    pass


class ClaudeFolderCorruptedError(Exception):
    """Raised when .claude folder structure is corrupted or invalid."""
    pass


def detect_claude_folder(repo_path: Path) -> Path:
    """
    Detect and validate .claude folder in repository.

    Args:
        repo_path: Path to repository root

    Returns:
        Path to .claude folder

    Raises:
        ClaudeFolderNotFoundError: If .claude folder doesn't exist
        ClaudeFolderCorruptedError: If .claude folder structure is invalid
    """
    claude_path = repo_path / ".claude"

    if not claude_path.exists():
        raise ClaudeFolderNotFoundError(f"No .claude folder found in {repo_path}")

    if not claude_path.is_dir():
        raise ClaudeFolderCorruptedError(f".claude exists but is not a directory in {repo_path}")

    # Validate basic structure - commands directory should exist or be creatable
    commands_path = claude_path / "commands"
    if not commands_path.exists():
        # This is okay - some .claude folders might not have commands yet
        pass
    elif not commands_path.is_dir():
        raise ClaudeFolderCorruptedError(f".claude/commands exists but is not a directory in {repo_path}")

    return claude_path


def get_claude_folder_info(claude_path: Path) -> Dict[str, any]:
    """
    Get information about a .claude folder.

    Args:
        claude_path: Path to .claude folder

    Returns:
        Dictionary with folder information
    """
    info = {
        "path": claude_path,
        "exists": claude_path.exists(),
        "size_bytes": 0,
        "command_count": 0,
        "has_settings": False,
        "has_local_settings": False,
        "files": []
    }

    if not claude_path.exists():
        return info

    # Calculate total size and file count
    for file_path in claude_path.rglob("*"):
        if file_path.is_file():
            info["files"].append(file_path.relative_to(claude_path))
            info["size_bytes"] += file_path.stat().st_size

            # Count command files
            if file_path.parent.name == "commands" and file_path.suffix == ".md":
                info["command_count"] += 1

    # Check for settings files
    info["has_settings"] = (claude_path / "settings.json").exists()
    info["has_local_settings"] = (claude_path / "settings.local.json").exists()

    return info


def create_backup(claude_path: Path) -> Path:
    """
    Create a backup of existing .claude folder.

    Args:
        claude_path: Path to .claude folder to backup

    Returns:
        Path to backup folder
    """
    if not claude_path.exists():
        raise ValueError(f"Cannot backup non-existent folder: {claude_path}")

    timestamp = int(time.time())
    backup_name = f".claude.backup.{timestamp}"
    backup_path = claude_path.parent / backup_name

    # Ensure backup name is unique
    counter = 1
    while backup_path.exists():
        backup_name = f".claude.backup.{timestamp}.{counter}"
        backup_path = claude_path.parent / backup_name
        counter += 1

    shutil.copytree(claude_path, backup_path)
    return backup_path


def copy_claude_folder(source_path: Path, target_repo: Path, create_backup_if_exists: bool = True) -> Dict[str, any]:
    """
    Copy .claude folder from source to target repository.

    Args:
        source_path: Path to source .claude folder
        target_repo: Path to target repository root
        create_backup_if_exists: Whether to backup existing .claude folder

    Returns:
        Dictionary with copy operation results
    """
    if not source_path.exists():
        raise ClaudeFolderNotFoundError(f"Source .claude folder does not exist: {source_path}")

    target_claude = target_repo / ".claude"
    backup_path = None

    result = {
        "success": False,
        "source": source_path,
        "target": target_claude,
        "backup_created": False,
        "backup_path": None,
        "files_copied": 0,
        "bytes_copied": 0,
        "error": None
    }

    try:
        # Create backup if target exists
        if target_claude.exists() and create_backup_if_exists:
            backup_path = create_backup(target_claude)
            result["backup_created"] = True
            result["backup_path"] = backup_path
            shutil.rmtree(target_claude)

        # Copy source to target
        shutil.copytree(source_path, target_claude)

        # Calculate copy statistics
        info = get_claude_folder_info(target_claude)
        result["files_copied"] = len(info["files"])
        result["bytes_copied"] = info["size_bytes"]
        result["success"] = True

    except Exception as e:
        result["error"] = str(e)
        # If we created a backup and copy failed, restore it
        if backup_path and backup_path.exists():
            if target_claude.exists():
                shutil.rmtree(target_claude)
            shutil.move(backup_path, target_claude)
            result["backup_created"] = False
            result["backup_path"] = None

    return result


def merge_claude_folders(source_path: Path, target_path: Path, preserve_local: bool = True) -> Dict[str, any]:
    """
    Merge source .claude folder into existing target .claude folder.

    Args:
        source_path: Path to source .claude folder
        target_path: Path to target .claude folder
        preserve_local: Whether to preserve local settings and customizations

    Returns:
        Dictionary with merge operation results
    """
    if not source_path.exists():
        raise ClaudeFolderNotFoundError(f"Source .claude folder does not exist: {source_path}")

    if not target_path.exists():
        # If target doesn't exist, just copy
        target_repo = target_path.parent
        return copy_claude_folder(source_path, target_repo, create_backup_if_exists=False)

    result = {
        "success": False,
        "files_updated": 0,
        "files_added": 0,
        "files_preserved": 0,
        "conflicts": [],
        "error": None
    }

    try:
        # Files to preserve during merge
        preserve_patterns = ["settings.local.json"] if preserve_local else []

        # Walk through source files
        for source_file in source_path.rglob("*"):
            if source_file.is_file():
                relative_path = source_file.relative_to(source_path)
                target_file = target_path / relative_path

                # Skip files we want to preserve
                if any(pattern in str(relative_path) for pattern in preserve_patterns):
                    result["files_preserved"] += 1
                    continue

                # Create parent directories if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)

                if target_file.exists():
                    # Check if files are different
                    if source_file.read_bytes() != target_file.read_bytes():
                        # For now, just overwrite. In a more sophisticated implementation,
                        # we might want to merge content or prompt user
                        shutil.copy2(source_file, target_file)
                        result["files_updated"] += 1
                    # If files are identical, no action needed
                else:
                    # New file, copy it
                    shutil.copy2(source_file, target_file)
                    result["files_added"] += 1

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def validate_claude_folder_structure(claude_path: Path) -> Dict[str, any]:
    """
    Validate .claude folder structure and report issues.

    Args:
        claude_path: Path to .claude folder

    Returns:
        Dictionary with validation results
    """
    validation = {
        "valid": True,
        "warnings": [],
        "errors": [],
        "structure": {
            "has_commands_dir": False,
            "command_count": 0,
            "has_settings": False,
            "has_local_settings": False,
            "total_files": 0
        }
    }

    if not claude_path.exists():
        validation["valid"] = False
        validation["errors"].append(".claude folder does not exist")
        return validation

    if not claude_path.is_dir():
        validation["valid"] = False
        validation["errors"].append(".claude exists but is not a directory")
        return validation

    # Check commands directory
    commands_path = claude_path / "commands"
    if commands_path.exists():
        if commands_path.is_dir():
            validation["structure"]["has_commands_dir"] = True
            # Count command files
            for cmd_file in commands_path.glob("*.md"):
                if cmd_file.is_file():
                    validation["structure"]["command_count"] += 1
        else:
            validation["valid"] = False
            validation["errors"].append("commands exists but is not a directory")
    else:
        validation["warnings"].append("No commands directory found")

    # Check settings files
    settings_path = claude_path / "settings.json"
    if settings_path.exists():
        if settings_path.is_file():
            validation["structure"]["has_settings"] = True
        else:
            validation["warnings"].append("settings.json exists but is not a file")

    local_settings_path = claude_path / "settings.local.json"
    if local_settings_path.exists():
        if local_settings_path.is_file():
            validation["structure"]["has_local_settings"] = True
        else:
            validation["warnings"].append("settings.local.json exists but is not a file")

    # Count total files
    validation["structure"]["total_files"] = sum(1 for f in claude_path.rglob("*") if f.is_file())

    return validation


def clean_claude_folder(claude_path: Path, remove_local_settings: bool = False) -> Dict[str, any]:
    """
    Clean up .claude folder by removing temporary and cache files.

    Args:
        claude_path: Path to .claude folder
        remove_local_settings: Whether to remove local settings files

    Returns:
        Dictionary with cleanup results
    """
    if not claude_path.exists():
        return {"success": False, "error": "Folder does not exist"}

    result = {
        "success": False,
        "files_removed": 0,
        "bytes_freed": 0,
        "error": None
    }

    try:
        patterns_to_remove = [
            "*.tmp",
            "*.cache",
            ".DS_Store",
            "Thumbs.db"
        ]

        if remove_local_settings:
            patterns_to_remove.append("settings.local.json")

        for pattern in patterns_to_remove:
            for file_path in claude_path.rglob(pattern):
                if file_path.is_file():
                    size = file_path.stat().st_size
                    file_path.unlink()
                    result["files_removed"] += 1
                    result["bytes_freed"] += size

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def get_repository_root(path: Path) -> Optional[Path]:
    """
    Find the root of a git repository by looking for .git directory.

    Args:
        path: Path to start searching from

    Returns:
        Path to repository root, or None if not in a git repository
    """
    current = path.resolve()

    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent

    return None


def is_git_repository(path: Path) -> bool:
    """
    Check if a path is within a git repository.

    Args:
        path: Path to check

    Returns:
        True if path is in a git repository
    """
    return get_repository_root(path) is not None