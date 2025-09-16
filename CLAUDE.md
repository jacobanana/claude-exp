# specli - Claude Command Deployer

A lightweight Python CLI tool for deploying and synchronizing Claude Code commands (.claude folders) across repositories. This tool enables developers to maintain consistent Claude commands across projects without manual copying.

## Overview

**specli** solves the problem of sharing and maintaining Claude Code commands across multiple projects. Instead of manually copying .claude folders or recreating commands from scratch, developers can use specli to deploy and update commands from a centralized source repository.

## Key Features

- **Deploy commands**: Copy .claude folders from source repository to target locations
- **Update commands**: Sync existing .claude folders with latest versions from source
- **GitHub integration**: Uses GitHub CLI for secure repository access and authentication
- **Path flexibility**: Deploy to current directory or specify custom target paths
- **Configuration persistence**: Remembers source repository for easy updates (SPEC-002)
- **Lightweight**: Minimal dependencies, focused functionality

## Toolchain (from SPEC-001)

This project follows a complete product development workflow:

1. **Business Specification**: Requirements captured in `specs/SPEC-001-claude-command-deployer.md`
2. **Technical Planning**: Implementation plan in `specs/PLAN-001-claude-command-deployer.md`
3. **TDD Implementation**: Test-driven development following structured phases
4. **Quality Assurance**: Comprehensive testing and validation against acceptance criteria

## Usage

### Deploy Commands
```bash
# Deploy to current directory
specli deploy https://github.com/user/source-repo

# Deploy to specific path
specli deploy https://github.com/user/source-repo --path /path/to/target

# Preview changes without making them
specli deploy https://github.com/user/source-repo --dry-run
```

### Update Commands
```bash
# Update using saved configuration (SPEC-002)
specli update

# Update with specific source
specli update --source https://github.com/user/source-repo

# Preview updates
specli update --dry-run
```

## Development Setup

This project uses **uv** for dependency management and development tooling:

### Environment Setup
```bash
# Install dependencies including dev tools
uv sync --group dev

# Activate virtual environment (optional)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Running Tests
```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_cli.py

# Run with verbose output
uv run pytest -v

# Run acceptance tests
uv run pytest tests/test_acceptance.py
```

### Code Quality
```bash
# Format code
uv run black .

# Check linting
uv run ruff check .

# Type checking (if available)
uv run mypy src/
```

### Running the Tool
```bash
# Install in development mode
uv pip install -e .

# Run directly with uv
uv run specli deploy <source-repo>
uv run specli update

# Or after installation
specli deploy <source-repo>
specli update
```

## Requirements

- **Python**: 3.8 or higher
- **GitHub CLI**: `gh` command must be installed and authenticated
- **uv**: For dependency management and development workflow
- **Repository access**: Read access to source repository, write access to target locations

## Project Structure

```
specli/
├── src/specli/          # Main source code
│   ├── main.py         # CLI entry point and commands
│   ├── filesystem.py   # File operations and .claude folder handling
│   ├── github.py       # GitHub CLI integration
│   └── config.py       # Configuration file management (SPEC-002)
├── tests/              # Test suite
│   ├── test_cli.py     # CLI command tests
│   ├── test_filesystem.py  # File operation tests
│   ├── test_github.py  # GitHub integration tests
│   └── test_acceptance.py  # End-to-end acceptance tests
├── specs/              # Product specifications and plans
└── pyproject.toml      # Project configuration and dependencies
```

## Authentication

The tool requires GitHub CLI authentication. Set up with:

```bash
# Login to GitHub
gh auth login

# Verify authentication
gh auth status
```

## Configuration

When you deploy commands, specli automatically creates a `specli.settings.json` file in the target directory to remember the source repository. This enables seamless updates without re-specifying the source.

Example configuration:
```json
{
  "source_repository": "https://github.com/user/source-repo",
  "deployed_at": "2024-01-15T10:30:00Z",
  "branch": "main"
}
```