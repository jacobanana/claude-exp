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