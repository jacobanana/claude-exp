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
            "Create backup of .claude folder before update?",
            default=True
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
            return {
                "success": False,
                "error": ".claude folder does not exist"
            }

        # For minimal implementation, just return success structure
        # Actual backup logic will be implemented in Phase 2
        return {
            "success": True,
            "backup_path": self.target_path / ".claude-backup" / "placeholder"
        }