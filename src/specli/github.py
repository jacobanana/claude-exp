"""
GitHub CLI integration for repository operations.

This module handles:
- GitHub CLI detection and version checking
- Authentication status and validation
- Repository access and validation
- Repository cloning and operations
- Error handling for GitHub operations
"""

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GitHubCLIError(Exception):
    """Base exception for GitHub CLI related errors."""

    pass


class GitHubCLINotFoundError(GitHubCLIError):
    """Raised when GitHub CLI is not installed or not found."""

    pass


class GitHubAuthenticationError(GitHubCLIError):
    """Raised when GitHub authentication fails or is missing."""

    pass


class GitHubRepositoryError(GitHubCLIError):
    """Raised when repository access or operations fail."""

    pass


def check_github_cli() -> Dict[str, any]:
    """
    Check if GitHub CLI is installed and get version information.

    Returns:
        Dictionary with CLI status and version info

    Raises:
        GitHubCLINotFoundError: If GitHub CLI is not installed
    """
    try:
        result = subprocess.run(
            ["gh", "--version"], capture_output=True, text=True, timeout=10
        )

        if result.returncode != 0:
            raise GitHubCLINotFoundError("GitHub CLI found but returned error")

        version_output = result.stdout.strip()
        # Parse version from output like "gh version 2.40.1 (2023-12-13)"
        version_match = re.search(r"gh version (\d+\.\d+\.\d+)", version_output)
        version = version_match.group(1) if version_match else "unknown"

        return {"installed": True, "version": version, "raw_output": version_output}

    except FileNotFoundError as e:
        raise GitHubCLINotFoundError("GitHub CLI (gh) is not installed or not in PATH") from e
    except subprocess.TimeoutExpired as e:
        raise GitHubCLINotFoundError("GitHub CLI check timed out") from e


def check_authentication() -> Dict[str, any]:
    """
    Check GitHub authentication status.

    Returns:
        Dictionary with authentication status and user info

    Raises:
        GitHubAuthenticationError: If authentication check fails
    """
    try:
        # Check auth status
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True, timeout=10
        )

        if result.returncode != 0:
            raise GitHubAuthenticationError(
                f"Not authenticated with GitHub: {result.stderr}"
            )

        # Get user info
        user_result = subprocess.run(
            ["gh", "api", "user"], capture_output=True, text=True, timeout=10
        )

        user_info = {}
        if user_result.returncode == 0:
            try:
                user_data = json.loads(user_result.stdout)
                user_info = {
                    "login": user_data.get("login"),
                    "id": user_data.get("id"),
                    "name": user_data.get("name"),
                }
            except json.JSONDecodeError:
                pass

        return {
            "authenticated": True,
            "status_output": result.stdout,
            "user": user_info,
        }

    except subprocess.TimeoutExpired as e:
        raise GitHubAuthenticationError("Authentication check timed out") from e


def parse_repository_url(repo_url: str) -> Tuple[str, str]:
    """
    Parse a repository URL or identifier to extract owner and repo name.

    Args:
        repo_url: Repository URL or identifier (various formats supported)

    Returns:
        Tuple of (owner, repo_name)

    Raises:
        ValueError: If URL format is not recognized
    """
    # Handle different formats:
    # - user/repo
    # - https://github.com/user/repo
    # - https://github.com/user/repo.git
    # - git@github.com:user/repo.git

    # Simple owner/repo format
    if "/" in repo_url and "://" not in repo_url and "@" not in repo_url:
        parts = repo_url.split("/")
        if len(parts) == 2:
            return parts[0], parts[1]

    # HTTPS URLs
    if repo_url.startswith("https://github.com/"):
        path = repo_url.replace("https://github.com/", "")
        if path.endswith(".git"):
            path = path[:-4]
        parts = path.split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]

    # SSH URLs
    if repo_url.startswith("git@github.com:"):
        path = repo_url.replace("git@github.com:", "")
        if path.endswith(".git"):
            path = path[:-4]
        parts = path.split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]

    raise ValueError(f"Unable to parse repository URL: {repo_url}")


def validate_repository_access(repo_url: str) -> Dict[str, any]:
    """
    Validate that a repository exists and is accessible.

    Args:
        repo_url: Repository URL or identifier

    Returns:
        Dictionary with repository information and access status

    Raises:
        GitHubRepositoryError: If repository validation fails
    """
    try:
        owner, repo = parse_repository_url(repo_url)
        repo_identifier = f"{owner}/{repo}"

        result = subprocess.run(
            ["gh", "api", f"repos/{repo_identifier}"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            if "404" in error_msg:
                raise GitHubRepositoryError(f"Repository not found: {repo_identifier}")
            elif "403" in error_msg:
                raise GitHubRepositoryError(
                    f"Access denied to repository: {repo_identifier}"
                )
            else:
                raise GitHubRepositoryError(
                    f"Failed to access repository {repo_identifier}: {error_msg}"
                )

        try:
            repo_data = json.loads(result.stdout)
            return {
                "accessible": True,
                "owner": repo_data.get("owner", {}).get("login"),
                "name": repo_data.get("name"),
                "full_name": repo_data.get("full_name"),
                "private": repo_data.get("private", False),
                "clone_url": repo_data.get("clone_url"),
                "permissions": repo_data.get("permissions", {}),
                "default_branch": repo_data.get("default_branch", "main"),
            }
        except json.JSONDecodeError as e:
            raise GitHubRepositoryError(
                f"Invalid response from GitHub API for {repo_identifier}"
            ) from e

    except ValueError as e:
        raise GitHubRepositoryError(str(e)) from e
    except subprocess.TimeoutExpired as e:
        raise GitHubRepositoryError(f"Repository validation timed out for {repo_url}") from e


def clone_repository(
    repo_url: str, target_dir: Optional[Path] = None
) -> Dict[str, any]:
    """
    Clone a repository using GitHub CLI.

    Args:
        repo_url: Repository URL or identifier
        target_dir: Directory to clone into (optional, uses temp dir if None)

    Returns:
        Dictionary with clone operation results

    Raises:
        GitHubRepositoryError: If cloning fails
    """
    if target_dir is None:
        target_dir = Path(tempfile.mkdtemp())
    else:
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

    try:
        owner, repo = parse_repository_url(repo_url)
        repo_identifier = f"{owner}/{repo}"

        # Change to target directory for cloning
        result = subprocess.run(
            ["gh", "repo", "clone", repo_identifier],
            capture_output=True,
            text=True,
            cwd=target_dir,
            timeout=300,  # 5 minutes for cloning
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            raise GitHubRepositoryError(
                f"Failed to clone {repo_identifier}: {error_msg}"
            )

        repo_path = target_dir / repo
        return {
            "success": True,
            "repository_path": repo_path,
            "target_directory": target_dir,
            "owner": owner,
            "repo_name": repo,
            "output": result.stdout,
        }

    except ValueError as e:
        raise GitHubRepositoryError(str(e)) from e
    except subprocess.TimeoutExpired as e:
        raise GitHubRepositoryError(f"Repository cloning timed out for {repo_url}") from e


def list_repository_contents(repo_url: str, path: str = "") -> List[Dict[str, any]]:
    """
    List contents of a repository directory.

    Args:
        repo_url: Repository URL or identifier
        path: Path within repository (empty for root)

    Returns:
        List of directory contents

    Raises:
        GitHubRepositoryError: If listing fails
    """
    try:
        owner, repo = parse_repository_url(repo_url)
        repo_identifier = f"{owner}/{repo}"

        endpoint = f"repos/{repo_identifier}/contents"
        if path:
            endpoint += f"/{path}"

        result = subprocess.run(
            ["gh", "api", endpoint], capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            raise GitHubRepositoryError(
                f"Failed to list contents of {repo_identifier}/{path}: {error_msg}"
            )

        try:
            contents = json.loads(result.stdout)
            if isinstance(contents, list):
                return [
                    {
                        "name": item.get("name"),
                        "type": item.get("type"),  # "file" or "dir"
                        "size": item.get("size", 0),
                        "path": item.get("path"),
                        "download_url": item.get("download_url"),
                    }
                    for item in contents
                ]
            else:
                # Single file response
                return [
                    {
                        "name": contents.get("name"),
                        "type": contents.get("type"),
                        "size": contents.get("size", 0),
                        "path": contents.get("path"),
                        "download_url": contents.get("download_url"),
                    }
                ]

        except json.JSONDecodeError as e:
            raise GitHubRepositoryError(
                f"Invalid response from GitHub API for {repo_identifier}/{path}"
            ) from e

    except ValueError as e:
        raise GitHubRepositoryError(str(e)) from e
    except subprocess.TimeoutExpired as e:
        raise GitHubRepositoryError(
            f"Repository contents listing timed out for {repo_url}"
        ) from e


def check_repository_has_claude_folder(repo_url: str) -> bool:
    """
    Check if a repository has a .claude folder.

    Args:
        repo_url: Repository URL or identifier

    Returns:
        True if .claude folder exists in repository
    """
    try:
        contents = list_repository_contents(repo_url)
        return any(
            item["name"] == ".claude" and item["type"] == "dir" for item in contents
        )
    except GitHubRepositoryError:
        return False


def get_repository_permissions(repo_url: str) -> Dict[str, bool]:
    """
    Get current user's permissions for a repository.

    Args:
        repo_url: Repository URL or identifier

    Returns:
        Dictionary with permission flags

    Raises:
        GitHubRepositoryError: If permission check fails
    """
    repo_info = validate_repository_access(repo_url)
    permissions = repo_info.get("permissions", {})

    return {
        "admin": permissions.get("admin", False),
        "push": permissions.get("push", False),
        "pull": permissions.get("pull", False),
        "maintain": permissions.get("maintain", False),
        "triage": permissions.get("triage", False),
    }


def validate_multiple_repositories(repo_urls: List[str]) -> Dict[str, any]:
    """
    Validate multiple repositories in batch.

    Args:
        repo_urls: List of repository URLs or identifiers

    Returns:
        Dictionary with validation results for each repository
    """
    results = {"valid_repositories": [], "invalid_repositories": [], "errors": {}}

    for repo_url in repo_urls:
        try:
            repo_info = validate_repository_access(repo_url)
            results["valid_repositories"].append({"url": repo_url, "info": repo_info})
        except GitHubRepositoryError as e:
            results["invalid_repositories"].append(repo_url)
            results["errors"][repo_url] = str(e)

    return results


def ensure_github_setup() -> Dict[str, any]:
    """
    Ensure GitHub CLI is properly set up and authenticated.

    Returns:
        Dictionary with setup status and information

    Raises:
        GitHubCLIError: If setup validation fails
    """
    setup_info = {
        "cli_installed": False,
        "cli_version": None,
        "authenticated": False,
        "user_info": {},
        "ready": False,
    }

    # Check CLI installation
    try:
        cli_info = check_github_cli()
        setup_info["cli_installed"] = True
        setup_info["cli_version"] = cli_info["version"]
    except GitHubCLINotFoundError as e:
        raise GitHubCLIError(f"GitHub CLI setup required: {e}") from e

    # Check authentication
    try:
        auth_info = check_authentication()
        setup_info["authenticated"] = True
        setup_info["user_info"] = auth_info["user"]
    except GitHubAuthenticationError as e:
        raise GitHubCLIError(f"GitHub authentication required: {e}") from e

    setup_info["ready"] = True
    return setup_info
