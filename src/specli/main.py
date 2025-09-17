"""
specli - Claude Command Deployer

A CLI tool for deploying and synchronizing .claude commands across repositories.
"""

from pathlib import Path

import click

from . import __version__
from .config import load_config
from .operations import deploy_operation, update_operation


@click.group()
@click.version_option(version=__version__)
def main():
    """Claude Command Deployer - Deploy and sync .claude commands across repositories."""
    pass


@main.command()
@click.argument("source_repo")
@click.option(
    "--path",
    default=".",
    help="Target path for deployment (defaults to current directory)",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def deploy(source_repo, path, dry_run):
    """Deploy .claude commands from source repository to target path."""
    # Output expected by tests
    click.echo(f"Deploy command called with source: {source_repo}")

    target_path = Path(path).resolve()
    click.echo(f"Target path: {target_path}")

    if dry_run:
        click.echo("Dry run mode - no changes would be made")

    # Delegate to business logic
    result = deploy_operation(source_repo, target_path, dry_run)

    # Format and display results
    if result["success"]:
        if dry_run:
            click.echo(f"   [DRY RUN] {result['message']}")
            if result.get("config_saved"):
                click.echo("   [DRY RUN] Configuration file created: specli.settings.json")
        else:
            if result.get("github_setup"):
                setup = result["github_setup"]
                click.echo("Checking GitHub CLI setup...")
                click.echo(f"GitHub CLI v{setup.get('cli_version', 'unknown')} authenticated as {setup.get('user_info', {}).get('login', 'unknown')}")

            if result.get("repository_validation"):
                click.echo(f"Validating source repository: {source_repo}")
                click.echo(f"Source repository validated: {result['repository_validation'].get('full_name', 'unknown')}")

            if result.get("claude_folder_found"):
                click.echo("Cloning source repository...")
                click.echo("Found .claude folder in source repository")
                click.echo(f"\nDeploying to target path: {target_path}")

            click.echo(result["message"])
            if result.get("files_copied", 0) > 0:
                click.echo(f"   Files copied: {result['files_copied']}")
                click.echo(f"   Bytes copied: {result['bytes_copied']}")

            if result.get("config_saved"):
                click.echo("Configuration saved: specli.settings.json")

        click.echo("\nDeploy operation completed!")
    else:
        click.echo(f"ERROR: {result.get('error', 'Unknown error')}")
        if result.get("error") and "GitHub CLI" in result["error"]:
            click.echo("Try running: gh auth login")


@main.command()
@click.option(
    "--path", default=".", help="Target path to update (defaults to current directory)"
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
@click.option(
    "--source",
    help="Source repository to pull updates from (will prompt if not specified)",
)
@click.option(
    "--no-backup", is_flag=True, help="Skip backup prompt and do not create backup"
)
def update(path, dry_run, source, no_backup):
    """Update existing .claude commands in target path."""
    # Output expected by tests
    target_path = Path(path).resolve()
    click.echo(f"Update command called for path: {target_path}")

    if dry_run:
        click.echo("Dry run mode - no changes would be made")

    # Handle source repository selection
    if not source:
        # Try to load from configuration file first
        config = load_config(target_path)
        if config["config_exists"] and config["repository_url"]:
            source = config["repository_url"]
            click.echo(f"Using saved repository from configuration: {source}")
        else:
            if config.get("error"):
                click.echo(f"Warning: Could not read configuration file: {config['error']}")
            else:
                click.echo("No configuration file found.")
            source = click.prompt("Enter source repository")

    # Delegate to business logic
    result = update_operation(target_path, source, dry_run, no_backup)

    # Format and display results
    if result["success"]:
        if dry_run:
            click.echo(f"   [DRY RUN] {result['message']}")
        else:
            # Show backup status
            if result.get("backup_needed"):
                click.echo("Found existing .claude folder in target")
                if result.get("backup_created"):
                    click.echo("Creating backup...")
                    click.echo("Backup created")
                else:
                    click.echo("Skipping backup as requested.")

            click.echo(f"\nUpdating target path: {target_path}")

            # Show key progress steps
            if result.get("github_setup"):
                click.echo("Checking GitHub CLI setup...")
            if result.get("repository_validation"):
                click.echo(f"Validating source repository: {source}")
            if result.get("claude_folder_found"):
                click.echo("Cloning source repository...")
                click.echo("Found .claude folder in source repository")

            # Show results
            click.echo(result["message"])
            if result.get("files_updated", 0) > 0:
                click.echo(f"   Files updated: {result['files_updated']}")
            if result.get("files_added", 0) > 0:
                click.echo(f"   Files added: {result['files_added']}")
            if result.get("files_preserved", 0) > 0:
                click.echo(f"   Files preserved: {result['files_preserved']}")

            if result.get("config_saved"):
                click.echo("Configuration updated: specli.settings.json")

        click.echo("\nUpdate operation completed!")
    else:
        # Handle errors
        if not result["path_validation"].get("path_exists"):
            click.echo(f"ERROR: Target path does not exist: {target_path}")
        elif not result["path_validation"].get("is_directory"):
            click.echo(f"ERROR: Target path is not a directory: {target_path}")
        else:
            click.echo(f"ERROR: {result.get('error', 'Unknown error')}")
            if result.get("error") and "GitHub CLI" in result["error"]:
                click.echo("Try running: gh auth login")


if __name__ == "__main__":
    main()
