# Implementation Plan — SPEC-004 Backup Functionality Consolidation

## Progress Tracking

### Validation Checklist
- [x] SPEC document exists and is readable
- [x] No "NEEDS CLARIFICATION" tags in the spec
- [x] All functional requirements are clear (refactor requirements)
- [x] All acceptance scenarios are complete
- [x] Technical approach is validated

### Implementation Progress
- [x] **Phase 0**: Environment & Setup ✅ Complete
- [ ] **Phase 1**: Baseline Validation
- [ ] **Phase 2**: Refactor Implementation (Validation Cycles)
- [ ] **Phase 3**: Integration Validation
- [ ] **Phase 4**: Acceptance Validation

---

## Specification Summary

**Refactor Goal**: Consolidate duplicate backup functionality by removing `create_backup()` from `filesystem.py` and using only `BackupManager` from `backup.py`.

**Key Requirements**:
- **FR-001**: Use only `BackupManager` class for all backup operations
- **FR-002**: Remove `create_backup()` function from `filesystem.py`
- **FR-003**: Update `copy_claude_folder()` to use `BackupManager`
- **FR-004**: Maintain backward compatibility for `create_backup_if_exists` parameter
- **FR-005**: Preserve existing backup storage behavior (`.claude-backup` directory)
- **FR-006**: Maintain all existing test coverage

**Success Criteria**: Single backup interface, reduced code duplication, all tests pass unchanged.

---

## Technical Approach Validation

### Current State Analysis
- **filesystem.py**: `create_backup()` creates backups in same directory with `.claude.backup.{timestamp}` naming
- **backup.py**: `BackupManager` creates backups in dedicated `.claude-backup/` folder with timestamped subdirectories
- **Usage**: `create_backup()` used only in `copy_claude_folder()`, `BackupManager` used in CLI `update` command
- **Tests**: 4 test files cover backup functionality (`test_backup.py`, `test_filesystem.py`, `test_cli.py`, `test_acceptance_backup.py`)

### Architecture Compatibility
✅ **Compatible**: Both implementations handle .claude folder backup
✅ **Risk Level**: Low - single usage point for `create_backup()`
✅ **Performance**: No impact - both use `shutil.copytree`
✅ **Team Capability**: Straightforward refactor within existing patterns

### Key Integration Points
1. **filesystem.py:171** - `backup_path = create_backup(target_claude)` needs replacement
2. **copy_claude_folder()** function interface must remain backward compatible
3. **Backup storage**: Must preserve `.claude-backup` directory structure from `BackupManager`

---

## Requirements Mapping

| Requirement | Implementation Tasks |
|-------------|---------------------|
| **FR-001** | IMPL-001, IMPL-002 |
| **FR-002** | IMPL-003 |
| **FR-003** | IMPL-001 |
| **FR-004** | IMPL-001, VAL-003 |
| **FR-005** | VAL-002, VAL-003 |
| **FR-006** | VAL-001, VAL-004 |

---

## Implementation Phases

### Phase 0: Environment & Setup
**Dependencies**: None

- **ENV-001**: Verify development environment setup
  - **Validation**: `uv sync --group dev` succeeds
  - **Expected Result**: All dev dependencies installed

- **ENV-002**: Setup quality measurement tools
  - **Validation**: Coverage and complexity tools available
  - **Expected Result**: Can measure code metrics baseline

### Phase 1: Baseline Validation
**Dependencies**: Phase 0 complete

- **VAL-BASE-001**: Run full existing test suite
  - **Command**: `uv run pytest`
  - **Expected Result**: All tests pass unchanged
  - **Covers**: FR-006 baseline

- **VAL-BASE-002**: Capture baseline metrics
  - **Metrics**: Test coverage %, code complexity, duplicate code detection
  - **Tools**: `pytest --cov`, complexity analysis
  - **Expected Result**: Baseline measurements for comparison

- **VAL-BASE-003**: Document current backup behavior differences
  - **Analysis**: Compare `create_backup()` vs `BackupManager.create_claude_backup()`
  - **Expected Result**: Clear understanding of behavior changes needed
  - **Covers**: FR-005 preparation

### Phase 2: Refactor Implementation (Validation Cycles)

#### Cycle 2.1: Update copy_claude_folder() to use BackupManager
**Dependencies**: Phase 1 complete

- **VAL-211**: Validate pre-refactor state
  - **Command**: `uv run pytest tests/test_filesystem.py -v`
  - **Expected Result**: All filesystem tests pass
  - **Covers**: FR-006

- **IMPL-001**: Modify copy_claude_folder() to use BackupManager
  - **File**: `src/specli/filesystem.py`
  - **Changes**:
    - Import `BackupManager` from `.backup`
    - Replace `create_backup(target_claude)` call with `BackupManager` usage
    - Adapt return values to match existing interface
    - Preserve `create_backup_if_exists` parameter behavior
  - **Covers**: FR-001, FR-003, FR-004
  - **Definition**: Replace filesystem.py:171 backup logic with BackupManager instantiation and call

- **VAL-212**: Validate post-modification state
  - **Command**: `uv run pytest tests/test_filesystem.py::test_copy_claude_folder* -v`
  - **Expected Result**: All copy_claude_folder tests pass unchanged
  - **Covers**: FR-004, FR-006

#### Cycle 2.2: Update backup storage behavior
**Dependencies**: Cycle 2.1 complete

- **VAL-221**: Validate current backup storage tests
  - **Command**: `uv run pytest tests/test_filesystem.py -k backup -v`
  - **Expected Result**: Identify tests that verify backup path structure
  - **Covers**: FR-005

- **IMPL-002**: Align backup path handling in copy_claude_folder()
  - **File**: `src/specli/filesystem.py`
  - **Changes**: Ensure backup_path in result dict points to correct BackupManager location
  - **Covers**: FR-001, FR-005
  - **Definition**: Update result["backup_path"] to use BackupManager's `.claude-backup` structure

- **VAL-222**: Validate backup storage behavior
  - **Test**: Create integration test to verify backup location
  - **Expected Result**: Backups created in `.claude-backup` directory structure
  - **Covers**: FR-005

#### Cycle 2.3: Remove create_backup() function
**Dependencies**: Cycle 2.2 complete

- **VAL-231**: Validate no remaining create_backup() usage
  - **Command**: `grep -r "create_backup(" src/ tests/`
  - **Expected Result**: Only usage should be in filesystem.py (soon to be removed)
  - **Covers**: FR-002

- **IMPL-003**: Remove create_backup() function from filesystem.py
  - **File**: `src/specli/filesystem.py`
  - **Changes**: Delete `create_backup()` function (lines 107-132)
  - **Covers**: FR-002
  - **Definition**: Complete removal of duplicate backup implementation

- **VAL-232**: Validate removal doesn't break anything
  - **Command**: `uv run pytest tests/test_filesystem.py -v`
  - **Expected Result**: All tests pass, no missing import errors
  - **Covers**: FR-002, FR-006

### Phase 3: Integration Validation
**Dependencies**: Phase 2 complete

- **VAL-301**: Run full test suite post-refactor
  - **Command**: `uv run pytest -v`
  - **Expected Result**: All tests pass unchanged
  - **Covers**: FR-006

- **VAL-302**: Verify CLI integration still works
  - **Command**: `uv run pytest tests/test_cli.py tests/test_acceptance_backup.py -v`
  - **Expected Result**: All CLI and acceptance tests pass
  - **Covers**: Integration between BackupManager usage points

- **VAL-303**: Code quality validation
  - **Commands**: `uv run ruff check .`, `uv run black --check .`
  - **Expected Result**: No new linting issues, formatting maintained
  - **Covers**: Code quality preservation

### Phase 4: Acceptance Validation
**Dependencies**: Phase 3 complete

- **VAL-401**: Acceptance Scenario 1 - copy_claude_folder() uses BackupManager
  - **Given**: Developer calls `copy_claude_folder()` with `create_backup_if_exists=True`
  - **When**: Target .claude folder exists
  - **Then**: System uses `BackupManager` instead of old `create_backup()`
  - **Test**: Inspect code and verify backup location in `.claude-backup`
  - **Covers**: Acceptance Scenario 1

- **VAL-402**: Acceptance Scenario 2 - Only BackupManager remains
  - **Given**: Refactor is complete
  - **When**: Searching codebase for backup functionality
  - **Then**: Only `BackupManager` from `backup.py` found, not `create_backup()` from `filesystem.py`
  - **Test**: `grep -r "def create_backup" src/` returns no results
  - **Covers**: Acceptance Scenario 2

- **VAL-403**: Acceptance Scenario 3 - All tests pass unchanged
  - **Given**: All tests run after refactor
  - **When**: Test suite completes
  - **Then**: All backup-related tests pass without modification
  - **Test**: Compare test results with baseline from VAL-BASE-001
  - **Covers**: Acceptance Scenario 3

---

## Risk Assessment

### High Priority Risks
1. **Backup Storage Location Change**:
   - **Risk**: Tests might expect `.claude.backup.{timestamp}` naming instead of `.claude-backup/{timestamp}/.claude`
   - **Mitigation**: Carefully review filesystem tests for hardcoded backup paths
   - **Detection**: VAL-221, VAL-222

2. **Interface Compatibility**:
   - **Risk**: `copy_claude_folder()` return values might change unexpectedly
   - **Mitigation**: Preserve exact return value structure, adapt BackupManager results
   - **Detection**: VAL-212

### Medium Priority Risks
1. **Import Circular Dependencies**:
   - **Risk**: Adding BackupManager import to filesystem.py could create cycles
   - **Mitigation**: Review import structure, BackupManager is already used in main.py
   - **Detection**: ENV-001 will catch import errors

2. **Test Coverage Gaps**:
   - **Risk**: Removing create_backup() might reduce test coverage
   - **Mitigation**: Ensure BackupManager tests cover equivalent scenarios
   - **Detection**: VAL-BASE-002 coverage comparison

---

## Effort Estimation

| Phase | Tasks | Estimated Time | Risk Level |
|-------|-------|----------------|------------|
| **Phase 0** | 2 tasks | 30 minutes | Low |
| **Phase 1** | 3 tasks | 45 minutes | Low |
| **Phase 2** | 9 tasks | 2.5 hours | Medium |
| **Phase 3** | 3 tasks | 45 minutes | Low |
| **Phase 4** | 3 tasks | 30 minutes | Low |
| **TOTAL** | **20 tasks** | **4.5 hours** | **Medium** |

### Parallel Work Opportunities
- VAL-BASE-002 and VAL-BASE-003 can run in parallel
- All VAL-2X1 validation steps can potentially run in parallel after IMPL tasks
- Phase 3 validation tasks can run in parallel

### Critical Dependencies
- Each IMPL task must complete before its corresponding VAL task
- Phase 2 cycles must complete sequentially (2.1 → 2.2 → 2.3)
- Phase 4 cannot start until Phase 3 completely passes

---

## Success Metrics

### Functional Success
- ✅ All existing tests pass unchanged (FR-006)
- ✅ Only BackupManager used for backup operations (FR-001)
- ✅ `create_backup()` function completely removed (FR-002)
- ✅ `copy_claude_folder()` maintains backward compatibility (FR-004)

### Quality Success
- ✅ Code duplication reduced (removed duplicate backup logic)
- ✅ Backup behavior consistent across all operations (FR-005)
- ✅ No new linting or formatting issues
- ✅ Test coverage maintained or improved

### Architectural Success
- ✅ Single source of truth for backup functionality
- ✅ Clear separation of concerns maintained
- ✅ No breaking changes to public interfaces