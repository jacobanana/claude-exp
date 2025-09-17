# Refactor Spec — Backup Functionality Consolidation

## 1. User Story (Single, focused story)
- **As a** developer maintaining the specli codebase
- **I want to** consolidate the duplicate backup functionality into a single, consistent implementation
- **So that** the codebase has reduced complexity, improved maintainability, and eliminates conflicting backup behaviors

## 2. Problem & Context
- **Developer Problem:** Two separate backup implementations exist with overlapping responsibilities and different interfaces, creating maintenance burden and potential inconsistencies
- **Current Situation:** `filesystem.py` contains a `create_backup()` function that creates timestamped backups in the same directory, while `backup.py` contains a `BackupManager` class that creates backups in a dedicated `.claude-backup` folder with user interaction prompts
- **Why This Matters Now:** The dual implementations create confusion about which backup method to use, increase maintenance overhead, and risk inconsistent backup behaviors across different operations

## 3. Refactoring Requirements (Must-haves only)
- **FR-001:** System MUST use only the `BackupManager` class from `backup.py` for all backup operations
- **FR-002:** System MUST remove the `create_backup()` function from `filesystem.py`
- **FR-003:** System MUST update all references to `create_backup()` in `copy_claude_folder()` to use `BackupManager`
- **FR-004:** System MUST maintain backward compatibility for the `copy_claude_folder()` function's `create_backup_if_exists` parameter
- **FR-005:** System MUST preserve existing backup storage behavior (`.claude-backup` directory structure)
- **FR-006:** System MUST maintain all existing test coverage for backup functionality

## 4. Acceptance Scenarios (Given / When / Then)
1. **Given** a developer calls `copy_claude_folder()` with `create_backup_if_exists=True`, **When** a target .claude folder exists, **Then** the system uses `BackupManager` to create a backup instead of the old `create_backup()` function
2. **Given** the refactor is complete, **When** searching the codebase for backup functionality, **Then** only `BackupManager` from `backup.py` should be found, not `create_backup()` from `filesystem.py`
3. **Given** all tests are run after the refactor, **When** the test suite completes, **Then** all backup-related tests must pass without modification

## 5. Success Criteria
- **User Success:** How will we know developers can achieve their goal after the refactor? The backup functionality will have a single, clear interface with consistent behavior across all operations
- **Business Success:** What measurable business outcome should improve? Reduced maintenance overhead and elimination of code duplication leading to faster development cycles

## 6. Scope Boundaries
- **In Scope:** `filesystem.py` `create_backup()` function removal, `copy_claude_folder()` function modification, import statement updates
- **Out of Scope:** Changes to `BackupManager` class interface, modification of backup storage format, changes to user-facing CLI behavior

## 7. Risks & Mitigations
- **Risk:** Breaking existing functionality that depends on the `create_backup()` function → **Mitigation:** Comprehensive test coverage verification and careful interface preservation
- **Risk:** Changing backup behavior in subtle ways that affect user experience → **Mitigation:** Maintain exact same backup storage structure and naming conventions

## 8. Questions & Clarifications
- Should the `create_backup_if_exists` parameter in `copy_claude_folder()` be renamed to better reflect the use of `BackupManager`?
    Let's use the names from BackupManager as the source of truth.
- Are there any performance considerations when switching from direct function calls to class-based backup management? 
    No.