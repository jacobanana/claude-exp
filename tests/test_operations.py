"""
Test module for operations business logic.

This module will contain tests for the extracted business logic operations
that will be independent of CLI concerns.
"""

import pytest
from pathlib import Path

from specli.operations import deploy_operation, update_operation


class TestOperationsInterface:
    """Test that operations module provides the required interface."""

    def test_deploy_operation_exists(self):
        """Test that deploy_operation function exists."""
        # This test MUST fail initially (Red phase)
        assert callable(deploy_operation)

    def test_deploy_operation_signature(self):
        """Test that deploy_operation has correct signature."""
        # Test the expected function signature for business logic
        # Should accept: source_repo, target_path, dry_run=False
        import inspect
        sig = inspect.signature(deploy_operation)
        params = list(sig.parameters.keys())

        assert "source_repo" in params
        assert "target_path" in params
        assert "dry_run" in params

    def test_update_operation_exists(self):
        """Test that update_operation function exists."""
        # This test MUST fail initially (Red phase)
        assert callable(update_operation)

    def test_update_operation_signature(self):
        """Test that update_operation has correct signature."""
        # Test the expected function signature for business logic
        # Should accept: target_path, source_repo=None, dry_run=False, no_backup=False
        import inspect
        sig = inspect.signature(update_operation)
        params = list(sig.parameters.keys())

        assert "target_path" in params
        assert "source_repo" in params
        assert "dry_run" in params
        assert "no_backup" in params


class TestOperationsReturnFormat:
    """Test that operations return expected format for testability."""

    def test_deploy_operation_returns_dict(self):
        """Test that deploy_operation returns a status dictionary."""
        # This should return a dict with success, message, and details
        result = deploy_operation("dummy_repo", Path("."), dry_run=True)

        assert isinstance(result, dict)
        assert "success" in result
        assert "message" in result
        assert isinstance(result["success"], bool)

    def test_update_operation_returns_dict(self):
        """Test that update_operation returns a status dictionary."""
        # This should return a dict with success, message, and details
        result = update_operation(Path("."), dry_run=True)

        assert isinstance(result, dict)
        assert "success" in result
        assert "message" in result
        assert isinstance(result["success"], bool)


class TestDeployOperationBusinessLogic:
    """Test the actual deploy business logic without CLI dependencies."""

    def test_deploy_operation_validates_github_setup(self):
        """Test that deploy operation validates GitHub CLI setup."""
        # This test MUST fail initially (Red phase)
        result = deploy_operation("https://github.com/test/repo", Path("/tmp/test"))

        # Should return validation results without CLI output
        assert "github_setup" in result
        assert "cli_version" in result["github_setup"]
        assert "user_info" in result["github_setup"]

    def test_deploy_operation_validates_repository_access(self):
        """Test that deploy operation validates repository access."""
        # This test MUST fail initially (Red phase)
        result = deploy_operation("https://github.com/test/repo", Path("/tmp/test"))

        # Should return repository validation without CLI output
        assert "repository_validation" in result
        # For invalid repos, should have error information
        if not result["success"]:
            assert "error" in result or "errors" in result
        else:
            assert "full_name" in result["repository_validation"]

    def test_deploy_operation_handles_claude_folder_detection(self):
        """Test that deploy operation detects .claude folder in source."""
        # This test MUST fail initially (Red phase)
        result = deploy_operation("https://github.com/test/repo", Path("/tmp/test"))

        # Should return claude folder detection results
        assert "claude_folder_found" in result
        assert isinstance(result["claude_folder_found"], bool)

    def test_deploy_operation_performs_file_operations(self):
        """Test that deploy operation performs file copy operations."""
        # This test MUST fail initially (Red phase)
        result = deploy_operation("https://github.com/test/repo", Path("/tmp/test"))

        # Should return file operation results
        assert "files_copied" in result
        assert "bytes_copied" in result
        assert isinstance(result["files_copied"], int)
        assert isinstance(result["bytes_copied"], int)

    def test_deploy_operation_saves_configuration(self):
        """Test that deploy operation saves configuration file."""
        # This test MUST fail initially (Red phase)
        result = deploy_operation("https://github.com/test/repo", Path("/tmp/test"))

        # Should return configuration save results
        assert "config_saved" in result
        assert isinstance(result["config_saved"], bool)

    def test_deploy_operation_dry_run_mode(self):
        """Test that deploy operation handles dry run mode correctly."""
        # This test MUST fail initially (Red phase)
        result = deploy_operation("https://github.com/test/repo", Path("/tmp/test"), dry_run=True)

        # In dry run, should not perform actual operations
        assert result["success"] is True
        assert "dry_run" in result
        assert result["dry_run"] is True
        assert result.get("files_copied", 0) == 0  # No actual copying in dry run

    def test_deploy_operation_error_handling(self):
        """Test that deploy operation handles errors without CLI dependencies."""
        # This test MUST fail initially (Red phase)
        result = deploy_operation("invalid-repo-url", Path("/tmp/test"))

        # Should return error information in structured format
        assert "success" in result
        assert "error" in result or "errors" in result
        # Should not raise exceptions, should return structured error info


class TestUpdateOperationBusinessLogic:
    """Test the actual update business logic without CLI dependencies."""

    def test_update_operation_validates_target_path(self):
        """Test that update operation validates target path existence."""
        # This test MUST fail initially (Red phase)
        result = update_operation(Path("/nonexistent/path"))

        # Should return validation results without CLI output
        assert "path_validation" in result
        assert "path_exists" in result["path_validation"]
        assert "is_directory" in result["path_validation"]

    def test_update_operation_loads_configuration(self):
        """Test that update operation loads configuration when no source provided."""
        # This test MUST fail initially (Red phase)
        result = update_operation(Path("."))

        # Should return configuration loading results
        assert "config_loaded" in result
        assert "source_from_config" in result

    def test_update_operation_handles_backup_logic(self):
        """Test that update operation handles backup creation logic."""
        # This test MUST fail initially (Red phase)
        result = update_operation(Path("."), no_backup=False)

        # Should return backup handling results
        assert "backup_needed" in result
        assert "backup_created" in result
        assert isinstance(result["backup_needed"], bool)
        assert isinstance(result["backup_created"], bool)

    def test_update_operation_performs_merge_operations(self):
        """Test that update operation performs merge operations."""
        # This test MUST fail initially (Red phase)
        result = update_operation(Path("."), source_repo="https://github.com/test/repo")

        # Should return merge operation results
        assert "files_updated" in result
        assert "files_added" in result
        assert "files_preserved" in result
        assert isinstance(result["files_updated"], int)
        assert isinstance(result["files_added"], int)
        assert isinstance(result["files_preserved"], int)

    def test_update_operation_saves_configuration(self):
        """Test that update operation saves configuration file."""
        # This test MUST fail initially (Red phase)
        result = update_operation(Path("."), source_repo="https://github.com/test/repo")

        # Should return configuration save results
        assert "config_saved" in result
        assert isinstance(result["config_saved"], bool)

    def test_update_operation_dry_run_mode(self):
        """Test that update operation handles dry run mode correctly."""
        # This test MUST fail initially (Red phase)
        result = update_operation(Path("."), dry_run=True)

        # In dry run, should not perform actual operations
        assert result["success"] is True
        assert "dry_run" in result
        assert result["dry_run"] is True
        assert result.get("files_updated", 0) == 0  # No actual updating in dry run

    def test_update_operation_no_backup_flag(self):
        """Test that update operation respects no_backup flag."""
        # This test MUST fail initially (Red phase)
        result = update_operation(Path("."), no_backup=True)

        # Should skip backup when no_backup=True
        assert "backup_needed" in result
        assert "backup_created" in result
        # If backup was needed but no_backup=True, backup_created should be False
        if result.get("backup_needed"):
            assert result["backup_created"] is False