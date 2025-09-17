"""
specli - Claude Command Deployer

A CLI tool for deploying and synchronizing .claude commands across repositories.
"""

from pathlib import Path

import click

from . import __version__
from .backup import BackupManager
from .config import load_config
from .filesystem import ClaudeFolderNotFoundError, detect_claude_folder
from .github import GitHubCLIError
from .operations import deploy_claude_commands, update_claude_commands
from .output import (
    format_config_message,
    format_dry_run_config_message,
    format_dry_run_message,
    format_error_message,
    format_github_setup_message,
    format_operation_details,
    format_repository_validation_message,
    format_success_message,
)
from .validation import (
    validate_github_setup,
    validate_source_repository,
    validate_target_path,
)


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
    try:
        # Output expected by tests
        click.echo(f"Deploy command called with source: {source_repo}")

        # Convert path to absolute path
        target_path = Path(path).resolve()
        click.echo(f"Target path: {target_path}")

        if dry_run:
            click.echo("Dry run mode - no changes would be made")
            click.echo(format_dry_run_message("deploy", str(target_path)))

            # Execute dry run through operations layer
            deploy_result = deploy_claude_commands(source_repo, target_path, dry_run)
            if deploy_result["success"]:
                details = deploy_result["details"]
                click.echo(
                    format_dry_run_config_message(
                        details["config_created"], details.get("config_file")
                    )
                )
            else:
                click.echo(format_dry_run_config_message(False))
            return

        # Validate GitHub setup
        click.echo("Checking GitHub CLI setup...")
        github_validation = validate_github_setup()
        if not github_validation["success"]:
            click.echo(format_error_message(github_validation["message"]))
            click.echo("Try running: gh auth login")
            return
        click.echo(format_github_setup_message(github_validation["setup_info"]))

        # Validate source repository
        click.echo(f"Validating source repository: {source_repo}")
        repo_validation = validate_source_repository(source_repo)
        if not repo_validation["success"]:
            click.echo(format_error_message(repo_validation["message"]))
            return
        click.echo(format_repository_validation_message(repo_validation["repo_info"]))

        # Perform deployment operation
        click.echo("Cloning source repository...")
        click.echo(f"\nDeploying to target path: {target_path}")

        # Execute deployment business logic
        deploy_result = deploy_claude_commands(source_repo, target_path, dry_run)

        if deploy_result["success"]:
            click.echo("Found .claude folder in source repository")
            details = deploy_result["details"]
            click.echo(format_success_message("deploy", details))

            # Display operation details
            for detail_line in format_operation_details("deploy", details):
                click.echo(detail_line)

            # Display configuration message
            config_msg = format_config_message(details, "deploy")
            if config_msg:
                click.echo(config_msg)
        else:
            click.echo(format_error_message(deploy_result["message"]))
            return

        click.echo("\nDeploy operation completed!")

    except GitHubCLIError as e:
        click.echo(format_error_message(f"GitHub CLI error: {e}"))
        click.echo("Try running: gh auth login")
    except Exception as e:
        click.echo(format_error_message(f"Unexpected error: {e}"))


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
    try:
        # Output expected by tests
        target_path = Path(path).resolve()
        click.echo(f"Update command called for path: {target_path}")

        if dry_run:
            click.echo("Dry run mode - no changes would be made")

        # Validate target path
        path_validation = validate_target_path(path)
        if not path_validation["success"]:
            click.echo(format_error_message(path_validation["message"]))
            return
        target_path = path_validation["resolved_path"]

        # Handle source repository selection
        if not source:
            # Try to load from configuration file first
            config = load_config(target_path)
            if config["config_exists"] and config["repository_url"]:
                source = config["repository_url"]
                click.echo(f"Using saved repository from configuration: {source}")
            else:
                if config.get("error"):
                    click.echo(
                        f"Warning: Could not read configuration file: {config['error']}"
                    )
                else:
                    click.echo("No configuration file found.")
                source = click.prompt("Enter source repository")

        # Update target path
        click.echo(f"\nUpdating target path: {target_path}")

        # Handle backup before update (if .claude folder exists)
        try:
            detect_claude_folder(target_path)
            click.echo("Found existing .claude folder in target")

            # Create backup manager and handle backup
            backup_manager = BackupManager(target_path)
            should_backup = backup_manager.should_create_backup(no_backup=no_backup)

            if should_backup and not dry_run:
                click.echo("Creating backup...")
                backup_result = backup_manager.create_claude_backup()

                if backup_result["success"]:
                    click.echo(f"Backup created: {backup_result['backup_path'].name}")
                else:
                    click.echo(f"ERROR: Backup failed: {backup_result['error']}")
                    click.echo("Update operation cancelled to protect your data.")
                    return
            elif should_backup and dry_run:
                click.echo("   [DRY RUN] Would create backup before update")
            elif not no_backup and not dry_run:
                click.echo("Skipping backup as requested.")

        except ClaudeFolderNotFoundError:
            # No .claude folder exists, no backup needed
            pass

        if dry_run:
            click.echo(format_dry_run_message("update", str(target_path)))
            return

        # Validate GitHub setup
        click.echo("Checking GitHub CLI setup...")
        github_validation = validate_github_setup()
        if not github_validation["success"]:
            click.echo(format_error_message(github_validation["message"]))
            click.echo("Try running: gh auth login")
            return
        click.echo(format_github_setup_message(github_validation["setup_info"]))

        # Validate source repository
        click.echo(f"Validating source repository: {source}")
        repo_validation = validate_source_repository(source)
        if not repo_validation["success"]:
            click.echo(format_error_message(repo_validation["message"]))
            return
        click.echo(format_repository_validation_message(repo_validation["repo_info"]))

        # Perform update operation
        click.echo("Cloning source repository...")

        # Execute update business logic
        update_result = update_claude_commands(target_path, source, dry_run, no_backup)

        if update_result["success"]:
            if not dry_run:
                click.echo("Found .claude folder in source repository")
                details = update_result["details"]

                if details.get("fresh_deploy"):
                    click.echo(
                        f"No existing .claude folder in {target_path}, deploying fresh copy..."
                    )

                click.echo(format_success_message("update", details))

                # Display operation details
                for detail_line in format_operation_details("update", details):
                    click.echo(detail_line)

                # Display configuration message
                config_msg = format_config_message(details, "update")
                if config_msg:
                    click.echo(config_msg)
        else:
            click.echo(format_error_message(update_result["message"]))
            return

        click.echo("\nUpdate operation completed!")

    except GitHubCLIError as e:
        click.echo(format_error_message(f"GitHub CLI error: {e}"))
        click.echo("Try running: gh auth login")
    except Exception as e:
        click.echo(format_error_message(f"Unexpected error: {e}"))


if __name__ == "__main__":
    main()
