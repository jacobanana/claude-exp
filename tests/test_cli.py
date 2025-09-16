"""
Test CLI command structure and interface.

Covers:
- FR-001: CLI tool with deploy/update commands
- FR-006: CLI arguments and interactive prompts
"""

import pytest
from pathlib import Path
from click.testing import CliRunner

from specli.main import main, deploy, update


class TestMainCLI:
    """Test main CLI group and basic functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_main_help(self):
        """Test main CLI help output."""
        result = self.runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Claude Command Deployer" in result.output
        assert "Deploy and sync .claude commands across" in result.output
        assert "repositories" in result.output
        assert "Commands:" in result.output
        assert "deploy" in result.output
        assert "update" in result.output

    def test_main_version(self):
        """Test version output."""
        result = self.runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "version 0.1.0" in result.output

    def test_main_no_command(self):
        """Test main CLI with no command shows help."""
        result = self.runner.invoke(main, [])

        # Click groups return exit code 0 when showing help
        # but in some versions it may return 2 for missing command
        assert result.exit_code in [0, 2]
        assert "Usage:" in result.output


class TestDeployCommand:
    """Test deploy command functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_deploy_help(self):
        """Test deploy command help output."""
        result = self.runner.invoke(deploy, ["--help"])

        assert result.exit_code == 0
        assert "Deploy .claude commands from source repository" in result.output
        assert "SOURCE_REPO" in result.output
        assert "--path" in result.output
        assert "--dry-run" in result.output

    def test_deploy_with_source_only(self):
        """Test deploy command with source only (defaults to current directory)."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(deploy, ["https://github.com/user/source.git"])

            assert result.exit_code == 0
            assert "Deploy command called with source: https://github.com/user/source.git" in result.output
            assert "Target path:" in result.output

    def test_deploy_with_path(self):
        """Test deploy command with source and target path."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(
                deploy,
                ["https://github.com/user/source.git", "--path", "/custom/path"]
            )

            assert result.exit_code == 0
            assert "Deploy command called with source: https://github.com/user/source.git" in result.output
            assert "Target path:" in result.output

    def test_deploy_dry_run(self):
        """Test deploy command with dry-run flag."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(
                deploy,
                ["https://github.com/user/source.git", "--dry-run"]
            )

            assert result.exit_code == 0
            assert "Dry run mode - no changes would be made" in result.output

    def test_deploy_missing_source(self):
        """Test deploy command without source repository fails."""
        result = self.runner.invoke(deploy, [])

        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_deploy_argument_validation(self):
        """Test deploy command argument validation."""
        with self.runner.isolated_filesystem():
            # Test with invalid source format (this will be validated later in implementation)
            result = self.runner.invoke(deploy, ["invalid-source"])

            # For now, just verify the command accepts the argument
            assert result.exit_code == 0
            assert "Deploy command called with source: invalid-source" in result.output
            assert "Target path:" in result.output


class TestUpdateCommand:
    """Test update command functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_update_help(self):
        """Test update command help output."""
        result = self.runner.invoke(update, ["--help"])

        assert result.exit_code == 0
        assert "Update existing .claude commands in target path" in result.output
        assert "--path" in result.output
        assert "--dry-run" in result.output

    def test_update_default_path(self):
        """Test update command with default path (current directory)."""
        result = self.runner.invoke(update, [])

        assert result.exit_code == 0
        assert "Update command called for path:" in result.output

    def test_update_with_path(self):
        """Test update command with custom path."""
        result = self.runner.invoke(update, ["--path", "/custom/path"])

        assert result.exit_code == 0
        assert "Update command called for path:" in result.output

    def test_update_dry_run(self):
        """Test update command with dry-run flag."""
        result = self.runner.invoke(update, ["--dry-run"])

        assert result.exit_code == 0
        assert "Dry run mode - no changes would be made" in result.output


class TestCLIIntegration:
    """Test CLI integration and command composition."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_main_deploy_integration(self):
        """Test deploy command through main CLI entry point."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(
                main,
                ["deploy", "https://github.com/user/source.git"]
            )

            assert result.exit_code == 0
            assert "Deploy command called with source: https://github.com/user/source.git" in result.output
            assert "Target path:" in result.output

    def test_main_update_integration(self):
        """Test update command through main CLI entry point."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ["update"])

            assert result.exit_code == 0
            assert "Update command called for path:" in result.output

    def test_invalid_command(self):
        """Test invalid command shows help."""
        result = self.runner.invoke(main, ["invalid-command"])

        assert result.exit_code != 0
        assert "No such command" in result.output

    def test_help_for_commands(self):
        """Test help works for all commands."""
        commands = ["deploy", "update"]

        for cmd in commands:
            result = self.runner.invoke(main, [cmd, "--help"])
            assert result.exit_code == 0
            assert "Usage:" in result.output


class TestConfigIntegration:
    """Test CLI integration with configuration file functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_deploy_creates_config_file(self):
        """Test that deploy command creates a configuration file."""
        with self.runner.isolated_filesystem():
            # Create a temporary directory for deployment target
            target_path = Path("./test_target").resolve()
            target_path.mkdir(exist_ok=True)

            # This test will initially fail because deploy command doesn't save config yet
            # We're mocking a successful deploy scenario by using dry-run to avoid GitHub API calls
            result = self.runner.invoke(
                deploy,
                ["https://github.com/user/source.git", "--path", str(target_path), "--dry-run"]
            )

            # Verify the command ran
            assert result.exit_code == 0

            # Check that config file was created
            config_file = target_path / "specli.settings.json"
            assert config_file.exists(), "Deploy command should create a configuration file"

            # If config file exists, verify its contents
            if config_file.exists():
                import json
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                assert config_data['repository_url'] == "https://github.com/user/source.git"
                assert 'deployed_at' in config_data

    def test_update_reads_config_file(self):
        """Test that update command reads configuration file when no source is provided."""
        with self.runner.isolated_filesystem():
            # Create a temporary directory with a config file
            target_path = Path("./test_target").resolve()
            target_path.mkdir(exist_ok=True)

            # Create a config file manually (simulating previous deploy)
            import json
            config_file = target_path / "specli.settings.json"
            config_data = {
                "repository_url": "https://github.com/user/saved-repo.git",
                "branch": None,
                "deployed_at": "2024-01-15T10:30:00Z"
            }
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)

            # Run update command without --source (should read from config)
            result = self.runner.invoke(
                update,
                ["--path", str(target_path), "--dry-run"]
            )

            # Verify the command ran
            assert result.exit_code == 0

            # This test will fail initially because update doesn't read config yet
            # The update command should use the repository from config file, not prompt for input
            assert "https://github.com/user/saved-repo.git" in result.output, "Update command should use repository from config file"