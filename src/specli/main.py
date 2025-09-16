"""
specli - Claude Command Deployer

A CLI tool for deploying and synchronizing .claude commands across repositories.
"""

import tempfile
from pathlib import Path

import click

from .backup import BackupManager
from .config import load_config, save_config
from .filesystem import (
    ClaudeFolderCorruptedError,
    ClaudeFolderNotFoundError,
    copy_claude_folder,
    detect_claude_folder,
    merge_claude_folders,
)
from .github import (
    GitHubCLIError,
    clone_repository,
    ensure_github_setup,
    validate_repository_access,
)


@click.group()
@click.version_option(version="0.1.0")
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
            # Save configuration file even for dry-run to show what would be created
            config_result = save_config(source_repo, target_path)
            if config_result["success"]:
                click.echo(
                    f"   [DRY RUN] Configuration file created: {config_result['config_file'].name}"
                )
            else:
                click.echo(
                    f"   [DRY RUN] Configuration file creation would fail: {config_result['error']}"
                )
            return

        # Validate GitHub setup
        click.echo("Checking GitHub CLI setup...")
        setup_info = ensure_github_setup()
        click.echo(
            f"GitHub CLI v{setup_info['cli_version']} authenticated as {setup_info['user_info'].get('login', 'unknown')}"
        )

        # Validate source repository
        click.echo(f"Validating source repository: {source_repo}")
        source_info = validate_repository_access(source_repo)
        click.echo(f"Source repository validated: {source_info['full_name']}")

        # Clone source repository to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            click.echo("Cloning source repository...")
            clone_result = clone_repository(source_repo, Path(temp_dir))
            source_repo_path = clone_result["repository_path"]

            # Detect .claude folder in source
            try:
                source_claude = detect_claude_folder(source_repo_path)
                click.echo("Found .claude folder in source repository")
            except ClaudeFolderNotFoundError:
                click.echo(
                    f"ERROR: No .claude folder found in source repository: {source_repo}"
                )
                return
            except ClaudeFolderCorruptedError as e:
                click.echo(f"ERROR: Corrupted .claude folder in source: {e}")
                return

            # Deploy to target path
            click.echo(f"\nDeploying to target path: {target_path}")

            if dry_run:
                click.echo(f"   [DRY RUN] Would deploy .claude folder to {target_path}")
                # Save configuration file even for dry-run to show what would be created
                config_result = save_config(source_repo, target_path)
                if config_result["success"]:
                    click.echo(
                        f"   [DRY RUN] Configuration file created: {config_result['config_file'].name}"
                    )
                else:
                    click.echo(
                        f"   [DRY RUN] Configuration file creation would fail: {config_result['error']}"
                    )
                return

            try:
                # Copy .claude folder to target path
                copy_result = copy_claude_folder(source_claude, target_path)

                if copy_result["success"]:
                    click.echo(f"Successfully deployed .claude folder to {target_path}")
                    click.echo(f"   Files copied: {copy_result['files_copied']}")
                    click.echo(f"   Bytes copied: {copy_result['bytes_copied']}")

                    if copy_result["backup_created"]:
                        click.echo(
                            f"   Backup created: {copy_result['backup_path'].name}"
                        )

                    # Save configuration file after successful deployment
                    config_result = save_config(source_repo, target_path)
                    if config_result["success"]:
                        click.echo(
                            f"Configuration saved: {config_result['config_file'].name}"
                        )
                    else:
                        click.echo(
                            f"Warning: Could not save configuration: {config_result['error']}"
                        )
                else:
                    click.echo(
                        f"ERROR: Failed to deploy to {target_path}: {copy_result['error']}"
                    )

            except Exception as e:
                click.echo(f"ERROR: Unexpected error: {e}")

        click.echo("\nDeploy operation completed!")

    except GitHubCLIError as e:
        click.echo(f"ERROR: GitHub CLI error: {e}")
        click.echo("Try running: gh auth login")
    except Exception as e:
        click.echo(f"ERROR: Unexpected error: {e}")


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

        # Ensure target path exists
        if not target_path.exists():
            click.echo(f"ERROR: Target path does not exist: {target_path}")
            return

        if not target_path.is_dir():
            click.echo(f"ERROR: Target path is not a directory: {target_path}")
            return

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
        backup_needed = False
        try:
            target_claude = detect_claude_folder(target_path)
            click.echo("Found existing .claude folder in target")
            backup_needed = True

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
            elif not no_backup:
                click.echo("Skipping backup as requested.")

        except ClaudeFolderNotFoundError:
            # No .claude folder exists, no backup needed
            pass

        if dry_run:
            click.echo(f"   [DRY RUN] Would update .claude folder in {target_path}")
            return

        # Validate GitHub setup
        click.echo("Checking GitHub CLI setup...")
        setup_info = ensure_github_setup()
        click.echo(
            f"GitHub CLI v{setup_info['cli_version']} authenticated as {setup_info['user_info'].get('login', 'unknown')}"
        )

        # Validate source repository
        click.echo(f"Validating source repository: {source}")
        source_info = validate_repository_access(source)
        click.echo(f"Source repository validated: {source_info['full_name']}")

        # Clone source repository to temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            click.echo("Cloning source repository...")
            clone_result = clone_repository(source, Path(temp_dir))
            source_repo_path = clone_result["repository_path"]

            # Detect .claude folder in source
            try:
                source_claude = detect_claude_folder(source_repo_path)
                click.echo("Found .claude folder in source repository")
            except ClaudeFolderNotFoundError:
                click.echo(
                    f"ERROR: No .claude folder found in source repository: {source}"
                )
                return
            except ClaudeFolderCorruptedError as e:
                click.echo(f"ERROR: Corrupted .claude folder in source: {e}")
                return

            try:
                # Check if target has .claude folder
                try:
                    target_claude = detect_claude_folder(target_path)
                    # Already announced in backup section

                    # Merge/update .claude folders
                    merge_result = merge_claude_folders(source_claude, target_claude)

                    if merge_result["success"]:
                        click.echo(
                            f"Successfully updated .claude folder in {target_path}"
                        )
                        click.echo(f"   Files updated: {merge_result['files_updated']}")
                        click.echo(f"   Files added: {merge_result['files_added']}")
                        click.echo(
                            f"   Files preserved: {merge_result['files_preserved']}"
                        )

                        # Save configuration file after successful update
                        config_result = save_config(source, target_path)
                        if config_result["success"]:
                            click.echo(
                                f"Configuration updated: {config_result['config_file'].name}"
                            )
                        else:
                            click.echo(
                                f"Warning: Could not update configuration: {config_result['error']}"
                            )
                    else:
                        click.echo(
                            f"ERROR: Failed to update {target_path}: {merge_result['error']}"
                        )

                except ClaudeFolderNotFoundError:
                    click.echo(
                        f"No existing .claude folder in {target_path}, deploying fresh copy..."
                    )
                    # If no existing .claude folder, do a fresh deploy
                    copy_result = copy_claude_folder(source_claude, target_path)

                    if copy_result["success"]:
                        click.echo(
                            f"Successfully deployed .claude folder to {target_path}"
                        )
                        click.echo(f"   Files copied: {copy_result['files_copied']}")
                        click.echo(f"   Bytes copied: {copy_result['bytes_copied']}")

                        # Save configuration file after successful deployment
                        config_result = save_config(source, target_path)
                        if config_result["success"]:
                            click.echo(
                                f"Configuration saved: {config_result['config_file'].name}"
                            )
                        else:
                            click.echo(
                                f"Warning: Could not save configuration: {config_result['error']}"
                            )
                    else:
                        click.echo(
                            f"ERROR: Failed to deploy to {target_path}: {copy_result['error']}"
                        )

            except Exception as e:
                click.echo(f"ERROR: Unexpected error: {e}")

        click.echo("\nUpdate operation completed!")

    except GitHubCLIError as e:
        click.echo(f"ERROR: GitHub CLI error: {e}")
        click.echo("Try running: gh auth login")
    except Exception as e:
        click.echo(f"ERROR: Unexpected error: {e}")


if __name__ == "__main__":
    main()
