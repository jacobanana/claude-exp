"""
Backup management for .claude folder protection.

This module provides backup functionality to protect user customizations
during update operations. It handles:
- Interactive user prompting for backup creation
- Timestamped backup storage in .claude-backup folder
- Safety checks to ensure backups complete before updates
"""

from pathlib import Path
from typing import Dict, Any
import click
import shutil
import time


class BackupManager:
    """
    Manages backup operations for .claude folders.

    Provides functionality to:
    - Prompt users for backup confirmation
    - Create timestamped backups in .claude-backup directory
    - Handle backup failures safely
    """

    def __init__(self, target_path: Path):
        """
        Initialize BackupManager for a target directory.

        Args:
            target_path: Path to directory containing .claude folder
        """
        self.target_path = target_path

    def should_create_backup(self, no_backup: bool = False) -> bool:
        """
        Determine if a backup should be created.

        Args:
            no_backup: If True, skip prompting and return False

        Returns:
            True if backup should be created, False otherwise
        """
        if no_backup:
            return False

        return click.confirm(
            "Create backup of .claude folder before update?", default=True
        )

    def create_claude_backup(self) -> Dict[str, Any]:
        """
        Create a timestamped backup of the .claude folder.

        Returns:
            Dictionary with backup operation results:
            - success: bool indicating if backup succeeded
            - backup_path: Path to created backup (if successful)
            - error: Error message (if failed)
        """
        claude_folder = self.target_path / ".claude"

        if not claude_folder.exists():
            return {"success": False, "error": ".claude folder does not exist"}

        try:
            # Create .claude-backup directory if it doesn't exist
            backup_root = self.target_path / ".claude-backup"
            backup_root.mkdir(exist_ok=True)

            # Generate unique timestamp-based backup name
            timestamp = int(time.time())
            backup_name = f"{timestamp}"
            backup_path = backup_root / backup_name

            # Ensure backup name is unique
            counter = 1
            while backup_path.exists():
                backup_name = f"{timestamp}_{counter}"
                backup_path = backup_root / backup_name
                counter += 1

            # Copy .claude folder to backup location
            shutil.copytree(claude_folder, backup_path / ".claude")

            return {"success": True, "backup_path": backup_path}

        except Exception as e:
            return {"success": False, "error": f"Backup failed: {str(e)}"}
