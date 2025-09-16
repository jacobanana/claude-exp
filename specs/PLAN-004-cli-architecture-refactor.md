# Implementation Plan: CLI Architecture Refactor

## Progress Tracking
**Instructions for Claude Code**: Before starting any task, you MUST:
1. Verify all prerequisites are marked as ✅ COMPLETE
2. Update task status to 🔄 IN PROGRESS when starting
3. Update task status to ✅ COMPLETE when finished
4. Validate all task requirements before marking complete

## Specification Summary
Refactor the current `main.py` file to separate CLI presentation logic from business operations. The goal is to extract business logic into dedicated modules, reduce CLI function complexity to under 50 lines each, and ensure all functionality remains testable without CLI mocking.

## Technical Approach Validation
**Proposed Architecture**:
- **operations.py**: Core business logic for deploy and update operations
- **cli_utils.py**: Shared CLI utilities (output formatting, error handling)
- **main.py**: Thin CLI layer (argument parsing, command delegation)

**Technology Stack**: No new dependencies required - refactoring existing Python/Click codebase.

**Risk Assessment**:
- **Low Risk**: Pure refactoring without changing external dependencies
- **Mitigation**: Comprehensive test coverage to prevent behavioral regressions
- **Validation**: Existing tests must continue to pass throughout refactor

## Requirements Mapping
| Requirement | Tasks |
|-------------|-------|
| FR-001: CLI delegates to business logic | IMPL-2A1, IMPL-2B1 |
| FR-002: Business logic testable without CLI | TEST-2A1, TEST-2B1 |
| FR-003: Extract common operations | IMPL-2C1 |
| FR-004: CLI handles only presentation | IMPL-2A1, IMPL-2B1 |
| FR-005: Preserve existing behavior | All VAL-xxx tasks |

## Implementation Phases

### Phase 0: Environment & Setup ✅ COMPLETE
**Status**: ✅ COMPLETE
**Dependencies**: None
**All tasks can run in parallel**

- [x] **ENV-001**: Run existing test suite to establish baseline
  - **Status**: ✅ COMPLETE
  - **Validation**: Baseline established - 124 passed, 2 failed (version tests), 1 skipped

- [x] **ENV-002**: Create test directory structure for new modules
  - **Status**: ✅ COMPLETE
  - **Validation**: `tests/test_operations.py` and `tests/test_cli_utils.py` exist

### Phase 1: Initial Test Structure ✅ COMPLETE
**Status**: ✅ COMPLETE
**Dependencies**: Phase 0 ✅ COMPLETE
**TDD Rule**: Create failing tests for core structure only

- [x] **TEST-001**: Write failing tests for operations module structure
  - **Status**: ✅ COMPLETE
  - **Prerequisites**: Phase 0 ✅ COMPLETE
  - **Covers**: Basic interfaces for FR-001, FR-002
  - **Expected Result**: Tests MUST fail (Red phase)
  - **Validation**: ✅ Tests failed with ModuleNotFoundError as expected

- [x] **IMPL-001**: Create minimal operations.py structure
  - **Status**: ✅ COMPLETE
  - **Prerequisites**: TEST-001 ✅ COMPLETE (and failing)
  - **Expected Result**: Phase 1 tests pass, no additional functionality
  - **Validation**: ✅ All 6 operations tests pass, functions return placeholder values

### Phase 2: Feature Implementation (TDD Cycles) ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 1 ✅ COMPLETE

#### TDD Cycle 2A: Deploy Operation Extraction ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED

- [ ] **TEST-2A1**: Write failing test for deploy business logic
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 1 ✅ COMPLETE
  - **Covers**: FR-001, FR-002 for deploy operation
  - **Expected Result**: New test MUST fail, existing tests still pass
  - **Validation**: Run test suite - TEST-2A1 fails, others pass

- [ ] **IMPL-2A1**: Extract deploy business logic to operations.py
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2A1 ✅ COMPLETE (and failing)
  - **Expected Result**: TEST-2A1 passes, all tests pass
  - **Validation**: Run full test suite - all tests pass

- [ ] **REFACTOR-2A1**: Refactor deploy CLI command to delegate to operations
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2A1 ✅ COMPLETE (all tests passing)
  - **Expected Result**: Deploy CLI function under 50 lines, all tests still pass
  - **Validation**: Line count < 50, run full test suite - all tests pass

#### TDD Cycle 2B: Update Operation Extraction ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 2A ✅ COMPLETE

- [ ] **TEST-2B1**: Write failing test for update business logic
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 2A ✅ COMPLETE
  - **Covers**: FR-001, FR-002 for update operation
  - **Expected Result**: New test MUST fail, existing tests still pass
  - **Validation**: Run test suite - TEST-2B1 fails, others pass

- [ ] **IMPL-2B1**: Extract update business logic to operations.py
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2B1 ✅ COMPLETE (and failing)
  - **Expected Result**: TEST-2B1 passes, all tests pass
  - **Validation**: Run full test suite - all tests pass

- [ ] **REFACTOR-2B1**: Refactor update CLI command to delegate to operations
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2B1 ✅ COMPLETE (all tests passing)
  - **Expected Result**: Update CLI function under 50 lines, all tests still pass
  - **Validation**: Line count < 50, run full test suite - all tests pass

#### TDD Cycle 2C: Common Operations Extraction ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 2B ✅ COMPLETE

- [ ] **TEST-2C1**: Write failing test for shared CLI utilities
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 2B ✅ COMPLETE
  - **Covers**: FR-003, FR-004 for common operations
  - **Expected Result**: New test MUST fail, existing tests still pass
  - **Validation**: Run test suite - TEST-2C1 fails, others pass

- [ ] **IMPL-2C1**: Extract common utilities to cli_utils.py
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2C1 ✅ COMPLETE (and failing)
  - **Expected Result**: TEST-2C1 passes, all tests pass
  - **Validation**: Run full test suite - all tests pass

- [ ] **REFACTOR-2C1**: Update CLI commands to use shared utilities
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2C1 ✅ COMPLETE (all tests passing)
  - **Expected Result**: Eliminated code duplication, all tests still pass
  - **Validation**: No duplicate code patterns, run full test suite - all tests pass

### Phase 3: Integration Testing ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 2 ✅ COMPLETE

#### TDD Cycle 3A: Integration Tests ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED

- [ ] **TEST-3A1**: Write failing integration tests for refactored architecture
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 2 ✅ COMPLETE
  - **Expected Result**: Integration tests MUST fail initially
  - **Validation**: Run integration tests - must fail

- [ ] **IMPL-3A1**: Implement integration logic between CLI and operations
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-3A1 ✅ COMPLETE (and failing)
  - **Expected Result**: All tests pass (unit + integration)
  - **Validation**: Run complete test suite - all pass

### Phase 4: Acceptance Validation ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 3 ✅ COMPLETE

- [ ] **VAL-001**: Validate business logic tests run without CLI mocking
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 3 ✅ COMPLETE
  - **Covers**: Acceptance scenario 1
  - **Validation**: Run operations tests independently - no CLI dependencies

- [ ] **VAL-002**: Validate new operation can be added independently
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 3 ✅ COMPLETE
  - **Covers**: Acceptance scenario 2
  - **Validation**: Add simple test operation without touching CLI code

- [ ] **VAL-003**: Validate existing CLI functionality unchanged
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 3 ✅ COMPLETE
  - **Covers**: Acceptance scenario 3
  - **Validation**: Run manual CLI tests, compare outputs to baseline

- [ ] **VAL-004**: Validate centralized error handling
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 3 ✅ COMPLETE
  - **Covers**: Acceptance scenario 4
  - **Validation**: Verify error handling logic exists in single location

- [ ] **VAL-005**: Validate CLI function line counts under 50
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 3 ✅ COMPLETE
  - **Covers**: Acceptance scenario 5
  - **Validation**: Count lines in deploy/update functions - both < 50 lines

## Task Status Legend
- ⬜ NOT STARTED: Task not yet begun
- 🔄 IN PROGRESS: Currently working on task
- ✅ COMPLETE: Task finished and validated
- ❌ BLOCKED: Cannot proceed due to failed prerequisites

## Progress Summary
**Total Tasks**: 20
**Completed**: 4 ✅
**In Progress**: 0 🔄
**Remaining**: 16 ⬜
**Blocked**: 0 ❌

## Risk Assessment
**Technical Risks**:
- **Behavioral Changes**: Risk of breaking existing CLI behavior during refactor
  - **Mitigation**: Comprehensive test coverage and baseline validation
- **Test Coupling**: Risk of tests still being coupled to CLI after refactor
  - **Mitigation**: Strict TDD approach with independent business logic tests

**Implementation Risks**:
- **Incomplete Extraction**: Risk of leaving business logic in CLI layer
  - **Mitigation**: Line count validation and code review
- **Over-Engineering**: Risk of creating unnecessary abstractions
  - **Mitigation**: Focus on simple separation, avoid premature optimization

## Effort Estimation
**Timeline**: 2-3 development sessions
**Complexity**: Medium - straightforward refactoring with clear boundaries
**Dependencies**: None - can proceed immediately with existing codebase