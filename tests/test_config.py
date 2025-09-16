"""
Test configuration file operations.

Covers:
- FR-001: Create config file when deploying commands
- FR-002: Read config file during update operations
- FR-004: Store config file in deployment location
- FR-005: Override saved repository with new source
"""

import pytest
from pathlib import Path
import tempfile
import json

from specli.config import save_config, load_config


class TestConfigurationModuleStructure:
    """Test basic configuration module interface exists."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir)

    def test_save_config_function_exists(self):
        """Test that save_config function exists and can be called."""
        # This should not raise an AttributeError
        assert callable(save_config)

    def test_load_config_function_exists(self):
        """Test that load_config function exists and can be called."""
        # This should not raise an AttributeError
        assert callable(load_config)

    def test_save_config_accepts_parameters(self):
        """Test that save_config accepts repository URL and target path."""
        # This should not raise a TypeError
        result = save_config("https://github.com/user/repo", self.config_path)
        assert result is not None

    def test_load_config_accepts_parameters(self):
        """Test that load_config accepts target path."""
        # This should not raise a TypeError
        result = load_config(self.config_path)
        assert result is not None

    def test_save_config_returns_success_status(self):
        """Test that save_config returns a dictionary with success status."""
        result = save_config("https://github.com/user/repo", self.config_path)
        assert isinstance(result, dict)
        assert 'success' in result

    def test_load_config_returns_configuration_data(self):
        """Test that load_config returns configuration data."""
        result = load_config(self.config_path)
        assert isinstance(result, dict)


class TestConfigurationBasicBehavior:
    """Test basic configuration behavior without actual file operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir)

    def test_save_config_with_minimal_parameters(self):
        """Test save_config with just repository URL and path."""
        result = save_config("https://github.com/user/repo", self.config_path)
        assert result['success'] is True or result['success'] is False

    def test_save_config_with_optional_branch(self):
        """Test save_config with optional branch parameter."""
        result = save_config(
            "https://github.com/user/repo",
            self.config_path,
            branch="main"
        )
        assert result['success'] is True or result['success'] is False

    def test_load_config_from_empty_directory(self):
        """Test load_config when no configuration exists."""
        result = load_config(self.config_path)
        # Should return some kind of result, even if config doesn't exist
        assert isinstance(result, dict)

    def test_config_functions_handle_pathlib_paths(self):
        """Test that config functions work with pathlib.Path objects."""
        path_obj = Path(self.temp_dir)

        save_result = save_config("https://github.com/user/repo", path_obj)
        assert isinstance(save_result, dict)

        load_result = load_config(path_obj)
        assert isinstance(load_result, dict)


class TestConfigurationFileSaving:
    """Test actual configuration file creation and saving."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir)
        self.config_file = self.config_path / "specli.settings.json"

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_config_creates_json_file(self):
        """Test that save_config actually creates a JSON file."""
        repository_url = "https://github.com/user/test-repo"

        result = save_config(repository_url, self.config_path)

        # Verify the operation was successful
        assert result['success'] is True

        # Verify the file was actually created
        assert self.config_file.exists()
        assert self.config_file.is_file()

    def test_save_config_creates_valid_json_content(self):
        """Test that save_config creates valid JSON with correct structure."""
        repository_url = "https://github.com/user/test-repo"
        branch = "main"

        result = save_config(repository_url, self.config_path, branch=branch)

        # Verify file exists and contains valid JSON
        assert self.config_file.exists()

        with open(self.config_file, 'r') as f:
            config_data = json.load(f)

        # Verify required fields are present
        assert config_data['repository_url'] == repository_url
        assert config_data['branch'] == branch
        assert 'deployed_at' in config_data

        # Verify timestamp format (should be ISO format)
        from datetime import datetime
        datetime.fromisoformat(config_data['deployed_at'].replace('Z', '+00:00'))

    def test_save_config_without_branch(self):
        """Test save_config works without optional branch parameter."""
        repository_url = "https://github.com/user/test-repo"

        result = save_config(repository_url, self.config_path)

        assert self.config_file.exists()

        with open(self.config_file, 'r') as f:
            config_data = json.load(f)

        assert config_data['repository_url'] == repository_url
        assert config_data['branch'] is None
        assert 'deployed_at' in config_data

    def test_save_config_overwrites_existing_file(self):
        """Test that save_config overwrites existing configuration file."""
        # Create initial config
        repository_url_1 = "https://github.com/user/repo1"
        save_config(repository_url_1, self.config_path)

        # Verify initial content
        with open(self.config_file, 'r') as f:
            initial_data = json.load(f)
        assert initial_data['repository_url'] == repository_url_1

        # Overwrite with new config
        repository_url_2 = "https://github.com/user/repo2"
        save_config(repository_url_2, self.config_path, branch="develop")

        # Verify new content overwrote the old
        with open(self.config_file, 'r') as f:
            new_data = json.load(f)
        assert new_data['repository_url'] == repository_url_2
        assert new_data['branch'] == "develop"

    def test_save_config_creates_nonexistent_directory(self):
        """Test save_config creates nonexistent directories automatically."""
        nonexistent_path = self.config_path / "nonexistent" / "directory"
        repository_url = "https://github.com/user/test-repo"

        result = save_config(repository_url, nonexistent_path)

        # Should create the directory and succeed
        assert result['success'] is True
        assert nonexistent_path.exists()
        assert (nonexistent_path / "specli.settings.json").exists()

    def test_save_config_handles_permission_denied(self):
        """Test save_config behavior when file creation is denied."""
        # This test is platform-specific and may not work on all systems
        import os
        if os.name == 'nt':  # Windows
            # Skip this test on Windows due to permission model differences
            pytest.skip("Permission test not applicable on Windows")

        # Make directory read-only
        os.chmod(self.config_path, 0o444)

        try:
            repository_url = "https://github.com/user/test-repo"
            result = save_config(repository_url, self.config_path)

            # Should handle the error gracefully
            assert result['success'] is False
            assert 'error' in result
        finally:
            # Restore permissions for cleanup
            os.chmod(self.config_path, 0o755)


class TestConfigurationFileReading:
    """Test actual configuration file reading and loading."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir)
        self.config_file = self.config_path / "specli.settings.json"

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_config_reads_existing_file(self):
        """Test that load_config reads an existing configuration file."""
        # Create a config file first
        repository_url = "https://github.com/user/test-repo"
        branch = "main"
        save_config(repository_url, self.config_path, branch=branch)

        # Now load it
        result = load_config(self.config_path)

        # Verify the loaded data
        assert result['config_exists'] is True
        assert result['repository_url'] == repository_url
        assert result['branch'] == branch
        assert 'deployed_at' in result

    def test_load_config_handles_missing_file(self):
        """Test load_config behavior when no configuration file exists."""
        result = load_config(self.config_path)

        # Should indicate no config exists
        assert result['config_exists'] is False
        assert result['repository_url'] is None
        assert result['branch'] is None
        assert result['config_file'] == self.config_file

    def test_load_config_reads_file_without_branch(self):
        """Test load_config reads configuration saved without branch."""
        repository_url = "https://github.com/user/test-repo"
        save_config(repository_url, self.config_path)  # No branch specified

        result = load_config(self.config_path)

        assert result['config_exists'] is True
        assert result['repository_url'] == repository_url
        assert result['branch'] is None

    def test_load_config_validates_json_structure(self):
        """Test load_config validates the JSON structure is correct."""
        repository_url = "https://github.com/user/test-repo"
        save_config(repository_url, self.config_path, branch="develop")

        result = load_config(self.config_path)

        # Check all expected fields are present
        assert 'repository_url' in result
        assert 'branch' in result
        assert 'deployed_at' in result
        assert 'config_exists' in result
        assert 'config_file' in result

        # Verify field values
        assert result['repository_url'] == repository_url
        assert result['branch'] == "develop"

    def test_load_config_handles_corrupted_json(self):
        """Test load_config behavior with corrupted JSON file."""
        # Create a corrupted JSON file
        with open(self.config_file, 'w') as f:
            f.write("{ invalid json content")

        result = load_config(self.config_path)

        # Should handle the error gracefully
        assert result['config_exists'] is False
        assert 'error' in result

    def test_load_config_handles_invalid_json_structure(self):
        """Test load_config behavior with valid JSON but wrong structure."""
        # Create JSON with wrong structure
        invalid_config = {"wrong_field": "wrong_value"}
        with open(self.config_file, 'w') as f:
            json.dump(invalid_config, f)

        result = load_config(self.config_path)

        # Should handle the invalid structure
        assert result['config_exists'] is False
        assert 'error' in result

    def test_load_config_preserves_file_path_info(self):
        """Test that load_config returns file path information."""
        result = load_config(self.config_path)

        assert result['config_file'] == self.config_file
        assert str(self.config_path) in str(result['config_file'])

    def test_load_config_multiple_reads_consistent(self):
        """Test that multiple reads of the same config return consistent data."""
        repository_url = "https://github.com/user/test-repo"
        save_config(repository_url, self.config_path, branch="main")

        result1 = load_config(self.config_path)
        result2 = load_config(self.config_path)

        # Results should be identical
        assert result1['repository_url'] == result2['repository_url']
        assert result1['branch'] == result2['branch']
        assert result1['deployed_at'] == result2['deployed_at']


class TestConfigurationOverride:
    """Test repository override functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir)
        self.config_file = self.config_path / "specli.settings.json"

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_override_existing_repository_url(self):
        """Test that new repository URL overwrites existing one."""
        # Save initial configuration
        original_repo = "https://github.com/user/original-repo"
        save_config(original_repo, self.config_path, branch="main")

        # Load to verify initial state
        initial_config = load_config(self.config_path)
        assert initial_config['repository_url'] == original_repo
        assert initial_config['branch'] == "main"

        # Override with new repository (add small delay to ensure different timestamp)
        import time
        time.sleep(1)
        new_repo = "https://github.com/user/new-repo"
        save_config(new_repo, self.config_path, branch="develop")

        # Load and verify override worked
        updated_config = load_config(self.config_path)
        assert updated_config['repository_url'] == new_repo
        assert updated_config['branch'] == "develop"
        # Timestamp should be updated
        assert updated_config['deployed_at'] != initial_config['deployed_at']

    def test_override_preserves_file_location(self):
        """Test that override operations preserve the config file location."""
        original_repo = "https://github.com/user/original-repo"
        save_config(original_repo, self.config_path)

        new_repo = "https://github.com/user/new-repo"
        result = save_config(new_repo, self.config_path)

        # File should still be in the same location
        assert result['config_file'] == self.config_file
        assert self.config_file.exists()

    def test_override_from_branch_to_no_branch(self):
        """Test overriding configuration from having a branch to no branch."""
        # Initial config with branch
        save_config("https://github.com/user/repo", self.config_path, branch="feature")
        initial_config = load_config(self.config_path)
        assert initial_config['branch'] == "feature"

        # Override without branch
        save_config("https://github.com/user/repo", self.config_path)
        updated_config = load_config(self.config_path)
        assert updated_config['branch'] is None

    def test_override_from_no_branch_to_branch(self):
        """Test overriding configuration from no branch to having a branch."""
        # Initial config without branch
        save_config("https://github.com/user/repo", self.config_path)
        initial_config = load_config(self.config_path)
        assert initial_config['branch'] is None

        # Override with branch
        save_config("https://github.com/user/repo", self.config_path, branch="main")
        updated_config = load_config(self.config_path)
        assert updated_config['branch'] == "main"

    def test_multiple_overrides(self):
        """Test multiple consecutive overrides work correctly."""
        repos = [
            "https://github.com/user/repo1",
            "https://github.com/user/repo2",
            "https://github.com/user/repo3"
        ]

        # Apply multiple overrides
        for i, repo in enumerate(repos):
            branch = f"branch-{i}" if i % 2 == 0 else None
            save_config(repo, self.config_path, branch=branch)

            # Verify each override worked
            config = load_config(self.config_path)
            assert config['repository_url'] == repo
            assert config['branch'] == branch

        # Final verification
        final_config = load_config(self.config_path)
        assert final_config['repository_url'] == repos[-1]
        assert final_config['branch'] == "branch-2"  # Last branch was branch-2

    def test_override_handles_same_repository_different_branch(self):
        """Test overriding with same repository but different branch."""
        repo_url = "https://github.com/user/test-repo"

        # Initial save
        save_config(repo_url, self.config_path, branch="main")
        initial_config = load_config(self.config_path)

        # Override with same repo, different branch (add small delay)
        import time
        time.sleep(1)
        save_config(repo_url, self.config_path, branch="develop")
        updated_config = load_config(self.config_path)

        # Repository should be same, branch should be updated
        assert updated_config['repository_url'] == repo_url
        assert updated_config['branch'] == "develop"
        assert updated_config['deployed_at'] != initial_config['deployed_at']