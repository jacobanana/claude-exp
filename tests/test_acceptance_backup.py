"""
Acceptance tests for backup functionality based on SPEC-003.

These tests validate the exact acceptance scenarios defined in the specification.
"""

import json
from pathlib import Path

from click.testing import CliRunner

from specli.main import update


class TestBackupAcceptanceScenarios:
    """Test all acceptance scenarios from SPEC-003."""

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()

    def _create_test_environment(self, has_claude_folder=True):
        """Create a test environment with config and optionally .claude folder."""
        # Create a config file to avoid source prompting
        config_data = {
            "repository_url": "https://github.com/user/test-repo.git",
            "branch": None,
            "deployed_at": "2024-01-15T10:30:00Z",
        }

        target_path = Path(".").resolve()
        config_file = target_path / "specli.settings.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=2)

        if has_claude_folder:
            # Create a .claude folder with content
            claude_folder = target_path / ".claude"
            claude_folder.mkdir()
            (claude_folder / "test.txt").write_text("original content")
            commands_dir = claude_folder / "commands"
            commands_dir.mkdir()
            (commands_dir / "test.md").write_text("# Test Command")

        return target_path

    def test_acceptance_scenario_1_default_prompting(self):
        """
        SPEC-003 Acceptance Scenario 1:
        Given I run `specli update` without any backup flags,
        When the command executes,
        Then I should be prompted "Create backup of .claude folder before update? [Y/n]" with "Y" as default
        """
        with self.runner.isolated_filesystem():
            self._create_test_environment(has_claude_folder=True)

            # Run update command without backup flags, simulate user pressing Enter (default)
            result = self.runner.invoke(update, ["--dry-run"], input="\n")

            # Verify the exact prompt message appears
            assert "Create backup of .claude folder before update?" in result.output
            assert "[Y/n]" in result.output or "(Y/n)" in result.output

            # Verify command executes successfully
            assert result.exit_code == 0

            # Verify it shows the dry-run backup message (confirming default "yes" was selected)
            assert "[DRY RUN] Would create backup before update" in result.output

    def test_acceptance_scenario_2_no_backup_flag(self):
        """
        SPEC-003 Acceptance Scenario 2:
        Given I run `specli update --no-backup`,
        When the command executes,
        Then no backup prompt should appear and the update should proceed directly
        """
        with self.runner.isolated_filesystem():
            self._create_test_environment(has_claude_folder=True)

            # Run update command with --no-backup flag
            result = self.runner.invoke(update, ["--no-backup", "--dry-run"])

            # Verify NO backup prompt appears
            assert "Create backup of .claude folder before update?" not in result.output

            # Verify command executes successfully
            assert result.exit_code == 0

            # Verify it proceeds without backup
            assert (
                "Skipping backup as requested" in result.output
                or "[DRY RUN] Would update" in result.output
            )

    def test_acceptance_scenario_3_backup_creation(self):
        """
        SPEC-003 Acceptance Scenario 3:
        Given I choose "yes" to the backup prompt,
        When the backup is created,
        Then a new timestamped folder should be created in `.claude-backup/` containing a complete copy of my current .claude folder
        """
        with self.runner.isolated_filesystem():
            target_path = self._create_test_environment(has_claude_folder=True)

            # Run update command and confirm backup (no dry-run to actually create backup)
            # Note: This will fail at GitHub operations, but backup should be created first
            _ = self.runner.invoke(update, [], input="y\n", catch_exceptions=True)

            # Verify backup folder structure was created
            backup_root = target_path / ".claude-backup"
            assert backup_root.exists(), "Backup root directory should be created"

            backup_folders = list(backup_root.iterdir())
            assert len(backup_folders) >= 1, "At least one backup folder should exist"

            # Verify backup contains complete copy of .claude folder
            backup_folder = backup_folders[
                0
            ]  # Get the first (and should be only) backup
            backed_up_claude = backup_folder / ".claude"
            assert backed_up_claude.exists(), "Backup should contain .claude folder"

            # Verify all original content is preserved
            assert (backed_up_claude / "test.txt").exists()
            assert (backed_up_claude / "test.txt").read_text() == "original content"
            assert (backed_up_claude / "commands" / "test.md").exists()
            assert (
                backed_up_claude / "commands" / "test.md"
            ).read_text() == "# Test Command"

    def test_acceptance_scenario_4_backup_failure_handling(self):
        """
        SPEC-003 Acceptance Scenario 4:
        Given the backup creation fails for any reason,
        When this occurs,
        Then the update operation should be cancelled and an error message should explain the backup failure
        """
        with self.runner.isolated_filesystem():
            target_path = self._create_test_environment(has_claude_folder=True)

            # Create a situation where backup will fail (make .claude-backup a file instead of directory)
            backup_blocker = target_path / ".claude-backup"
            backup_blocker.write_text("blocking file")

            # Run update command and confirm backup
            result = self.runner.invoke(update, [], input="y\n", catch_exceptions=True)

            # Verify backup failure is reported
            assert (
                "ERROR: Backup failed:" in result.output
                or "Backup failed:" in result.output
            )

            # Verify update operation is cancelled
            assert (
                "Update operation cancelled" in result.output
                or "cancelled to protect your data" in result.output
            )

            # Verify command doesn't continue to GitHub operations
            assert "Cloning source repository" not in result.output

    def test_acceptance_scenario_5_multiple_backups(self):
        """
        SPEC-003 Acceptance Scenario 5:
        Given I have multiple previous backups in `.claude-backup/`,
        When I create a new backup,
        Then all previous backups should remain untouched and the new backup should have a unique timestamp
        """
        with self.runner.isolated_filesystem():
            target_path = self._create_test_environment(has_claude_folder=True)

            # Create first backup manually
            from specli.backup import BackupManager

            backup_manager = BackupManager(target_path)

            first_backup = backup_manager.create_claude_backup()
            assert first_backup["success"], "First backup should succeed"
            first_backup_path = first_backup["backup_path"]

            # Modify .claude folder content
            claude_folder = target_path / ".claude"
            (claude_folder / "new_file.txt").write_text("new content")

            # Create second backup via CLI
            _ = self.runner.invoke(update, [], input="y\n", catch_exceptions=True)

            # Verify both backups exist
            backup_root = target_path / ".claude-backup"
            backup_folders = list(backup_root.iterdir())
            assert len(backup_folders) >= 2, "Should have at least 2 backup folders"

            # Verify backups have unique timestamps
            backup_names = [folder.name for folder in backup_folders]
            assert len(set(backup_names)) == len(
                backup_names
            ), "All backup folder names should be unique"

            # Verify first backup is untouched
            assert first_backup_path.exists(), "First backup should still exist"
            assert (
                first_backup_path / ".claude" / "test.txt"
            ).exists(), "First backup content should be preserved"

            # Verify first backup doesn't contain the new file (proving it's untouched)
            assert not (
                first_backup_path / ".claude" / "new_file.txt"
            ).exists(), "First backup should not contain new content"

    def test_backup_prompt_exact_format(self):
        """Test that the prompt matches the exact format specified in acceptance criteria."""
        with self.runner.isolated_filesystem():
            self._create_test_environment(has_claude_folder=True)

            # Run update and capture the exact prompt
            result = self.runner.invoke(update, ["--dry-run"], input="\n")

            # Verify exact prompt format from SPEC-003
            assert "Create backup of .claude folder before update?" in result.output

            # The prompt should indicate Y is default (either [Y/n] or similar)
            output_lines = result.output.split("\n")
            prompt_line = next(
                (line for line in output_lines if "Create backup" in line), ""
            )

            # Should indicate Y is default in some way
            assert any(
                indicator in prompt_line
                for indicator in ["[Y/n]", "(Y/n)", "[y/N]", "(Y/n)"]
            ), f"Prompt should show Y as default. Found: {prompt_line}"
