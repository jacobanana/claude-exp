"""
Tests for backup manager functionality.

Tests the backup protection system that:
- Prompts users to create backups before updates
- Supports --no-backup flag to skip prompts
- Creates timestamped backups in .claude-backup folder
- Ensures backup completion before allowing updates
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from specli.backup import BackupManager


class TestBackupManagerInterface:
    """Test the basic interface and structure of BackupManager."""

    def test_backup_manager_can_be_imported(self):
        """BackupManager class should be importable from specli.backup module."""
        # This test will fail until BackupManager is implemented
        assert BackupManager is not None

    def test_backup_manager_can_be_instantiated(self):
        """BackupManager should be instantiable with a target path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir)
            backup_manager = BackupManager(target_path)
            assert backup_manager is not None
            assert backup_manager.target_path == target_path


class TestBackupManagerPrompting:
    """Test the interactive prompting functionality."""

    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.target_path = Path(self.temp_dir)
        self.backup_manager = BackupManager(self.target_path)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_should_create_backup_method_exists(self):
        """BackupManager should have should_create_backup method."""
        assert hasattr(self.backup_manager, "should_create_backup")
        assert callable(self.backup_manager.should_create_backup)

    @patch("click.confirm")
    def test_should_create_backup_prompts_user_with_correct_message(self, mock_confirm):
        """should_create_backup should prompt user with correct message and default."""
        mock_confirm.return_value = True

        result = self.backup_manager.should_create_backup()

        mock_confirm.assert_called_once_with(
            "Create backup of .claude folder before update?", default=True
        )
        assert result is True

    @patch("click.confirm")
    def test_should_create_backup_returns_user_choice(self, mock_confirm):
        """should_create_backup should return the user's choice."""
        mock_confirm.return_value = False

        result = self.backup_manager.should_create_backup()

        assert result is False

    def test_should_create_backup_respects_no_backup_flag(self):
        """should_create_backup should skip prompting when no_backup=True."""
        # This should not prompt user at all when no_backup=True
        result = self.backup_manager.should_create_backup(no_backup=True)
        assert result is False


class TestBackupManagerFolderOperations:
    """Test the backup folder creation and management."""

    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.target_path = Path(self.temp_dir)
        self.backup_manager = BackupManager(self.target_path)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_claude_backup_method_exists(self):
        """BackupManager should have create_claude_backup method."""
        assert hasattr(self.backup_manager, "create_claude_backup")
        assert callable(self.backup_manager.create_claude_backup)

    def test_create_claude_backup_creates_backup_folder_structure(self):
        """create_claude_backup should create .claude-backup directory structure."""
        # Create a .claude folder to backup
        claude_folder = self.target_path / ".claude"
        claude_folder.mkdir()
        (claude_folder / "test_file.txt").write_text("test content")

        result = self.backup_manager.create_claude_backup()

        # Should create .claude-backup folder
        backup_root = self.target_path / ".claude-backup"
        assert backup_root.exists()
        assert backup_root.is_dir()

        # Should create timestamped subfolder
        backup_folders = list(backup_root.iterdir())
        assert len(backup_folders) == 1
        assert backup_folders[0].is_dir()

        # Should return success status with backup path
        assert result["success"] is True
        assert "backup_path" in result
        assert result["backup_path"].parent == backup_root

    def test_create_claude_backup_preserves_folder_contents(self):
        """create_claude_backup should completely preserve .claude folder contents."""
        # Create a .claude folder with complex structure
        claude_folder = self.target_path / ".claude"
        claude_folder.mkdir()
        commands_dir = claude_folder / "commands"
        commands_dir.mkdir()
        (commands_dir / "test.md").write_text("# Test Command")
        (claude_folder / "settings.json").write_text('{"test": true}')

        result = self.backup_manager.create_claude_backup()

        # Verify backup contains all original content
        backup_path = result["backup_path"]
        assert (backup_path / ".claude" / "commands" / "test.md").exists()
        assert (backup_path / ".claude" / "settings.json").exists()
        assert (
            backup_path / ".claude" / "commands" / "test.md"
        ).read_text() == "# Test Command"
        assert (
            backup_path / ".claude" / "settings.json"
        ).read_text() == '{"test": true}'

    def test_create_claude_backup_handles_missing_claude_folder(self):
        """create_claude_backup should handle case where .claude folder doesn't exist."""
        # No .claude folder exists
        result = self.backup_manager.create_claude_backup()

        # Should return failure status
        assert result["success"] is False
        assert "error" in result
        assert ".claude folder does not exist" in result["error"]

    def test_create_claude_backup_generates_unique_timestamps(self):
        """create_claude_backup should generate unique timestamps for multiple backups."""
        # Create a .claude folder
        claude_folder = self.target_path / ".claude"
        claude_folder.mkdir()
        (claude_folder / "test.txt").write_text("content")

        # Create multiple backups
        result1 = self.backup_manager.create_claude_backup()
        result2 = self.backup_manager.create_claude_backup()

        # Should have different backup paths
        assert result1["success"] is True
        assert result2["success"] is True
        assert result1["backup_path"] != result2["backup_path"]

        # Both backups should exist
        assert result1["backup_path"].exists()
        assert result2["backup_path"].exists()


class TestBackupManagerSafety:
    """Test backup safety and error handling."""

    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.target_path = Path(self.temp_dir)
        self.backup_manager = BackupManager(self.target_path)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_claude_backup_returns_status_dict(self):
        """create_claude_backup should return a dictionary with success status."""
        claude_folder = self.target_path / ".claude"
        claude_folder.mkdir()

        result = self.backup_manager.create_claude_backup()

        assert isinstance(result, dict)
        assert "success" in result
        assert isinstance(result["success"], bool)

    def test_backup_failure_prevents_update_flow(self):
        """When backup fails, the system should indicate failure clearly."""
        # This test ensures backup failure is communicated properly
        result = self.backup_manager.create_claude_backup()

        # When .claude doesn't exist, backup should fail
        assert result["success"] is False
        # The calling code should check this status before proceeding
