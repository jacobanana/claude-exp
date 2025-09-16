# specli - Claude Command Deployer

A lightweight Python CLI tool for deploying and synchronizing Claude Code commands (.claude folders) across multiple repositories.

## Features

- **Deploy commands**: Copy .claude folders from source to target repositories
- **Update commands**: Sync existing .claude folders with latest versions
- **GitHub integration**: Uses GitHub CLI for secure repository access
- **Multi-target support**: Deploy to multiple repositories in one command
- **Interactive prompts**: User-friendly CLI with helpful prompts

## Installation

Install globally using pipx (recommended):

```bash
pipx install specli
```

Or install in current environment:

```bash
pip install specli
```

## Usage

### Deploy commands to repositories
```bash
# Deploy to specific repositories
specli deploy https://github.com/user/source-repo target-repo1 target-repo2

# Interactive mode (prompts for target repos)
specli deploy https://github.com/user/source-repo

# Dry run to see what would happen
specli deploy https://github.com/user/source-repo --dry-run
```

### Update existing commands
```bash
# Update specific repositories
specli update target-repo1 target-repo2

# Interactive mode
specli update

# Dry run
specli update --dry-run
```

## Requirements

- Python 3.8+
- GitHub CLI (`gh`) installed and authenticated
- Access to source and target repositories

## Development

This project uses UV for dependency management and development tooling:

```bash
# Install dependencies
uv sync --group dev

# Run tests
uv run pytest

# Format code
uv run black .

# Lint code
uv run ruff check .

# Install for development
uv pip install -e .
```

## Architecture

This project demonstrates a complete product development workflow:

- **Specification**: Business requirements in `specs/SPEC-001-*.md`
- **Planning**: Technical implementation plan in `specs/PLAN-001-*.md`
- **Implementation**: TDD-based development following the plan
- **Custom tooling**: Uses Claude Code commands for spec/plan generation