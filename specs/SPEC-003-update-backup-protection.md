# SPEC-003: Update Backup Protection

## User Story

**As a** developer using specli to manage Claude commands
**I want to** create backups of my .claude folder before updates
**So that** I don't lose any customizations or local changes when syncing with the source repository

## Problem & Context

**User Problem**: When updating Claude commands with `specli update`, users risk losing local modifications, customizations, or work-in-progress changes to their .claude folder. There's currently no protection against accidental data loss during updates.

**Current Situation**: Users must manually backup their .claude folders before running updates, or risk losing important customizations when the source repository overwrites local changes.

**Why This Matters**: Claude command folders often contain valuable customizations and work. Losing these changes due to an update can result in significant rework and frustration, especially when users forget to manually backup before updating.

## Functional Requirements

- **FR-001**: System MUST prompt users to create a backup before performing updates when no backup flag is specified
- **FR-002**: System MUST default to suggesting "yes" for backup creation (user can accept with Enter)
- **FR-003**: System MUST provide a `--no-backup` flag to skip backup prompts entirely
- **FR-004**: System MUST store all backups in a `.claude-backup` folder in the target directory
- **FR-005**: System MUST create timestamped backup folders to avoid overwriting previous backups
- **FR-006**: System MUST complete the backup successfully before proceeding with the update operation

## Acceptance Scenarios

1. **Given** I run `specli update` without any backup flags, **When** the command executes, **Then** I should be prompted "Create backup of .claude folder before update? [Y/n]" with "Y" as default
2. **Given** I run `specli update --no-backup`, **When** the command executes, **Then** no backup prompt should appear and the update should proceed directly
3. **Given** I choose "yes" to the backup prompt, **When** the backup is created, **Then** a new timestamped folder should be created in `.claude-backup/` containing a complete copy of my current .claude folder
4. **Given** the backup creation fails for any reason, **When** this occurs, **Then** the update operation should be cancelled and an error message should explain the backup failure
5. **Given** I have multiple previous backups in `.claude-backup/`, **When** I create a new backup, **Then** all previous backups should remain untouched and the new backup should have a unique timestamp

## Success Criteria

**User Success**: Users can confidently run updates knowing their customizations are protected, and can easily recover previous versions if needed.

**Business Success**: Reduced user frustration and support requests related to lost customizations during updates.

## Questions & Clarifications

**User Research Needed**:
- How often do users actually customize their .claude folders?
- What's the preferred timestamp format for backup folder names?

**Business Decisions Required**:
- Should there be a limit on how many backups to keep automatically?
- Should backups be cleaned up automatically after a certain time period?

**Assumptions to Validate**:
- Users prefer an interactive prompt over always creating backups
- Timestamped folders are sufficient for backup organization
- The `.claude-backup` folder name won't conflict with existing tooling