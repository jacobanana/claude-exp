# Implementation Plan: Update Backup Protection

## Progress Tracking
**Instructions for Claude Code**: Before starting any task, you MUST:
1. Verify all prerequisites are marked as ✅ COMPLETE
2. Update task status to 🔄 IN PROGRESS when starting
3. Update task status to ✅ COMPLETE when finished
4. Validate all task requirements before marking complete

## Specification Summary
Implementing backup protection for the `specli update` command that prompts users to create backups before updates, supports a `--no-backup` flag, and stores all backups in timestamped folders within `.claude-backup` directory.

## Technical Approach Validation

**Technology Stack Analysis:**
- ✅ **Click CLI Framework**: Already in use, supports flag options and user prompts
- ✅ **Python 3.8+ with pathlib**: Established in project, perfect for file operations
- ✅ **Existing filesystem module**: Has backup functionality that can be extended
- ✅ **pytest + coverage**: Test framework already configured and working

**Architecture Compatibility:**
- ✅ The existing `update` command in `main.py:169` is where backup logic needs integration
- ✅ Current `filesystem.py` has `create_backup()` function but creates `.claude.backup.{timestamp}` format
- ✅ Need to extend/modify backup functionality to use `.claude-backup/` folder structure
- ✅ Click framework supports prompts via `click.prompt()` and `click.confirm()`

**Risk Assessment:**
- ⚠️ **Backup folder naming change**: Need to update from current `.claude.backup.{timestamp}` to `.claude-backup/{timestamp}/`
- ✅ **User interaction**: Click's `click.confirm()` provides exactly the needed functionality
- ✅ **Timestamp uniqueness**: Current implementation already handles collisions with counters

## Requirements Mapping

| Requirement | Implementation Tasks |
|-------------|---------------------|
| FR-001: Prompt users for backup when no flag | TEST-2A1, IMPL-2A1 |
| FR-002: Default to "yes" for backup | TEST-2A1, IMPL-2A1 |
| FR-003: Provide --no-backup flag | TEST-2B1, IMPL-2B1 |
| FR-004: Store backups in .claude-backup folder | TEST-2C1, IMPL-2C1 |
| FR-005: Create timestamped backup folders | TEST-2C1, IMPL-2C1 |
| FR-006: Complete backup before update | TEST-2D1, IMPL-2D1 |

## Implementation Phases

### Phase 0: Environment & Setup ✅ COMPLETE
**Status**: ✅ COMPLETE
**Dependencies**: None
**All tasks can run in parallel**

- [x] **ENV-001**: Verify development environment setup
  - **Status**: ✅ COMPLETE
  - **Definition**: Run `uv sync --group dev` and verify pytest, black, ruff are available
  - **Validation**: `uv run pytest --version` succeeds, `uv run black --version` succeeds, `uv run ruff --version` succeeds

- [x] **ENV-002**: Verify current test suite passes
  - **Status**: ✅ COMPLETE
  - **Definition**: Run `uv run pytest` to ensure baseline test suite is passing
  - **Validation**: All existing tests pass with 0 failures (102 passed, 1 skipped)

### Phase 1: Initial Test Structure ✅ COMPLETE
**Status**: ✅ COMPLETE
**Dependencies**: Phase 0 ✅ COMPLETE
**TDD Rule**: Create failing tests for core structure only

- [x] **TEST-001**: Write failing tests for backup manager interface
  - **Status**: ✅ COMPLETE
  - **Prerequisites**: Phase 0 ✅ COMPLETE
  - **Covers**: Basic structure for backup functionality
  - **Definition**: Create `tests/test_backup.py` with tests for `BackupManager` class interface (methods for prompting, creating backups in .claude-backup folder)
  - **Expected Result**: Tests MUST fail (Red phase)
  - **Validation**: Run `uv run pytest tests/test_backup.py` - verify they fail with import/class not found errors

- [x] **IMPL-001**: Implement minimal backup manager structure
  - **Status**: ✅ COMPLETE
  - **Prerequisites**: TEST-001 ✅ COMPLETE (and failing)
  - **Definition**: Create basic `BackupManager` class in `src/specli/backup.py` with empty method stubs
  - **Expected Result**: Phase 1 tests pass, no additional functionality
  - **Validation**: Run `uv run pytest tests/test_backup.py` - basic interface tests pass (10 passed, 3 failed for advanced features)

### Phase 2: Feature Implementation (TDD Cycles) ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 1 ✅ COMPLETE

#### TDD Cycle 2A: Interactive Backup Prompting ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED

- [ ] **TEST-2A1**: Write failing test for interactive backup prompting
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 1 ✅ COMPLETE
  - **Covers**: FR-001 (prompt when no flag), FR-002 (default to yes)
  - **Definition**: Write test that validates `should_create_backup()` method prompts user with correct message and defaults to "yes"
  - **Expected Result**: New test MUST fail, existing tests still pass
  - **Validation**: Run test suite - TEST-2A1 fails, others pass

- [ ] **IMPL-2A1**: Implement interactive backup prompting
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2A1 ✅ COMPLETE (and failing)
  - **Definition**: Implement `should_create_backup()` method using `click.confirm()` with correct prompt and default
  - **Expected Result**: TEST-2A1 passes, all tests pass
  - **Validation**: Run full test suite - all tests pass

- [ ] **REFACTOR-2A1**: Refactor backup prompting if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2A1 ✅ COMPLETE (all tests passing)
  - **Definition**: Improve code quality, extract constants for prompt message
  - **Expected Result**: Code improved, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

#### TDD Cycle 2B: No-Backup Flag Support ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 2A ✅ COMPLETE

- [ ] **TEST-2B1**: Write failing test for --no-backup flag
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 2A ✅ COMPLETE
  - **Covers**: FR-003 (--no-backup flag skips prompts)
  - **Definition**: Write test that validates when `no_backup=True` flag is passed, no prompting occurs
  - **Expected Result**: New test MUST fail, existing tests still pass
  - **Validation**: Run test suite - TEST-2B1 fails, others pass

- [ ] **IMPL-2B1**: Implement --no-backup flag logic
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2B1 ✅ COMPLETE (and failing)
  - **Definition**: Modify `should_create_backup()` to accept `no_backup` parameter and skip prompting when True
  - **Expected Result**: TEST-2B1 passes, all tests pass
  - **Validation**: Run full test suite - all tests pass

- [ ] **REFACTOR-2B1**: Refactor flag logic if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2B1 ✅ COMPLETE (all tests passing)
  - **Definition**: Clean up conditional logic, ensure clear parameter handling
  - **Expected Result**: Code improved, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

#### TDD Cycle 2C: Claude-Backup Folder Structure ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 2B ✅ COMPLETE

- [ ] **TEST-2C1**: Write failing test for .claude-backup folder structure
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 2B ✅ COMPLETE
  - **Covers**: FR-004 (store in .claude-backup), FR-005 (timestamped folders)
  - **Definition**: Write test that validates `create_claude_backup()` creates timestamped folders in `.claude-backup/` directory
  - **Expected Result**: New test MUST fail, existing tests still pass
  - **Validation**: Run test suite - TEST-2C1 fails, others pass

- [ ] **IMPL-2C1**: Implement .claude-backup folder structure
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2C1 ✅ COMPLETE (and failing)
  - **Definition**: Create `create_claude_backup()` method that creates `.claude-backup/{timestamp}/` folders and copies .claude contents
  - **Expected Result**: TEST-2C1 passes, all tests pass
  - **Validation**: Run full test suite - all tests pass

- [ ] **REFACTOR-2C1**: Refactor backup folder creation if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2C1 ✅ COMPLETE (all tests passing)
  - **Definition**: Extract timestamp formatting, ensure consistent directory structure
  - **Expected Result**: Code improved, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

#### TDD Cycle 2D: Backup Safety (Complete Before Update) ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 2C ✅ COMPLETE

- [ ] **TEST-2D1**: Write failing test for backup-before-update safety
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 2C ✅ COMPLETE
  - **Covers**: FR-006 (backup must complete before update proceeds)
  - **Definition**: Write test that validates update operation fails when backup creation fails
  - **Expected Result**: New test MUST fail, existing tests still pass
  - **Validation**: Run test suite - TEST-2D1 fails, others pass

- [ ] **IMPL-2D1**: Implement backup safety logic
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2D1 ✅ COMPLETE (and failing)
  - **Definition**: Modify backup creation to return success/failure status and handle failures in update flow
  - **Expected Result**: TEST-2D1 passes, all tests pass
  - **Validation**: Run full test suite - all tests pass

- [ ] **REFACTOR-2D1**: Refactor safety logic if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2D1 ✅ COMPLETE (all tests passing)
  - **Definition**: Ensure clean error handling, consistent return value structure
  - **Expected Result**: Code improved, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

### Phase 3: CLI Integration (TDD Cycles) ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 2 ✅ COMPLETE

#### TDD Cycle 3A: Update Command Integration ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED

- [ ] **TEST-3A1**: Write failing integration tests for update command
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 2 ✅ COMPLETE
  - **Covers**: End-to-end backup functionality in update command
  - **Definition**: Write CLI tests in `tests/test_cli.py` that validate `specli update` and `specli update --no-backup` commands
  - **Expected Result**: Integration tests MUST fail initially
  - **Validation**: Run integration tests - must fail with missing --no-backup option

- [ ] **IMPL-3A1**: Integrate backup logic into update command
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-3A1 ✅ COMPLETE (and failing)
  - **Definition**: Modify `update()` function in `main.py` to add `--no-backup` flag and call backup logic before merge operations
  - **Expected Result**: All tests pass (unit + integration)
  - **Validation**: Run complete test suite - all pass

- [ ] **REFACTOR-3A1**: Refactor CLI integration if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-3A1 ✅ COMPLETE (all tests passing)
  - **Definition**: Clean up update command flow, ensure backup happens at the right point
  - **Expected Result**: Code improved, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

### Phase 4: Acceptance Validation ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 3 ✅ COMPLETE

- [ ] **VAL-001**: Validate acceptance scenario 1 - Default prompting
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 3 ✅ COMPLETE
  - **Covers**: "Given I run `specli update` without flags, When command executes, Then I should be prompted 'Create backup of .claude folder before update? [Y/n]'"
  - **Definition**: Create acceptance test that verifies exact prompt message and default behavior
  - **Validation**: Manual test shows correct prompt, automated test validates prompt text

- [ ] **VAL-002**: Validate acceptance scenario 2 - No-backup flag
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-001 ✅ COMPLETE
  - **Covers**: "Given I run `specli update --no-backup`, When command executes, Then no backup prompt should appear"
  - **Definition**: Create acceptance test that verifies --no-backup skips all prompting
  - **Validation**: Automated test confirms no prompt interaction when flag is used

- [ ] **VAL-003**: Validate acceptance scenario 3 - Backup creation
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-002 ✅ COMPLETE
  - **Covers**: "Given I choose yes to backup prompt, When backup is created, Then timestamped folder created in .claude-backup/"
  - **Definition**: Create acceptance test that verifies backup folder structure and content completeness
  - **Validation**: Test confirms .claude-backup/{timestamp}/ folder contains complete copy

- [ ] **VAL-004**: Validate acceptance scenario 4 - Backup failure handling
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-003 ✅ COMPLETE
  - **Covers**: "Given backup creation fails, When this occurs, Then update operation cancelled with error message"
  - **Definition**: Create acceptance test that simulates backup failure and validates error handling
  - **Validation**: Test confirms update stops and error message explains backup failure

- [ ] **VAL-005**: Validate acceptance scenario 5 - Multiple backups
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-004 ✅ COMPLETE
  - **Covers**: "Given multiple previous backups exist, When I create new backup, Then all previous backups remain untouched"
  - **Definition**: Create acceptance test that verifies backup preservation across multiple operations
  - **Validation**: Test confirms all backup folders preserved with unique timestamps

## Task Status Legend
- ⬜ NOT STARTED: Task not yet begun
- 🔄 IN PROGRESS: Currently working on task
- ✅ COMPLETE: Task finished and validated
- ❌ BLOCKED: Cannot proceed due to failed prerequisites

## Progress Summary
**Total Tasks**: 21
**Completed**: 4 ✅
**In Progress**: 0 🔄
**Remaining**: 17 ⬜
**Blocked**: 0 ❌

## Risk Assessment

**Technical Risks:**
1. **Backup folder structure change**: Modifying from existing `.claude.backup.{timestamp}` to `.claude-backup/{timestamp}/` structure requires careful testing to ensure no conflicts
2. **CLI integration complexity**: Adding backup logic to existing update command flow needs careful placement to not disrupt current functionality
3. **User interaction testing**: Click prompt testing requires proper mocking and interaction simulation

**Mitigation Strategies:**
1. **Incremental TDD approach**: Each change is tested before implementation, reducing integration risk
2. **Existing test preservation**: All current tests must continue passing throughout implementation
3. **Backup structure validation**: Comprehensive tests for new folder structure before CLI integration

## Effort Estimation

**Overall Timeline**: 1-2 development sessions
**Resource Requirements**:
- 1 developer
- Existing Python/Click expertise
- Test-driven development discipline

**Phase Breakdown**:
- Phase 0 (Setup): 15 minutes
- Phase 1 (Structure): 30 minutes
- Phase 2 (Core Features): 90 minutes
- Phase 3 (CLI Integration): 45 minutes
- Phase 4 (Validation): 30 minutes

**Total Estimated Effort**: 3.5 hours