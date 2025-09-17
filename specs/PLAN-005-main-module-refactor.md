# Implementation Plan — Main Module Separation of Concerns

## Progress Tracking

### Phase 0: Environment & Setup
- [ ] **ENV-001**: Validate development environment setup
- [ ] **ENV-002**: Setup code quality tooling and baseline metrics
- [ ] **ENV-003**: Verify all dependencies and test framework

### Phase 1: Baseline Validation
- [ ] **VAL-BASE-001**: Run full existing test suite and capture passing state
- [ ] **VAL-BASE-002**: Capture baseline code quality metrics (complexity, duplication)

### Phase 2: Refactor Implementation (Validation Cycles)
- [ ] **CYCLE-001**: Extract common patterns and validation logic (FR-002)
- [ ] **CYCLE-002**: Separate CLI handlers from business operations (FR-001)
- [ ] **CYCLE-003**: Isolate output formatting and messaging (FR-003)
- [ ] **CYCLE-004**: Final integration and cleanup

### Phase 3: Integration Validation
- [ ] **VAL-INT-001**: Run comprehensive regression tests
- [ ] **VAL-INT-002**: Validate CLI behavior preservation

### Phase 4: Acceptance Validation
- [ ] **VAL-ACC-001**: Validate acceptance scenario 1 (identical CLI behavior)
- [ ] **VAL-ACC-002**: Validate acceptance scenario 2 (isolated business logic)
- [ ] **VAL-ACC-003**: Validate acceptance scenario 3 (testable components)
- [ ] **VAL-ACC-004**: Validate acceptance scenario 4 (reusable patterns)

---

## Specification Summary

**Objective**: Refactor main.py (354 lines) to separate CLI command handling from business logic, extract common patterns, and improve maintainability while preserving identical CLI behavior.

**Key Requirements**:
- **FR-001**: Separate CLI handlers from business logic
- **FR-002**: Extract common validation/error handling patterns
- **FR-003**: Isolate output formatting from operations
- **FR-004**: Maintain identical CLI interface (deploy, update, version, help)
- **FR-005**: Preserve all existing error messages and output formats

**Success Criteria**: Zero functional changes, improved testability, reduced code duplication

---

## Technical Approach Validation

### Current Architecture Analysis
- **main.py**: 354 lines containing CLI commands, business logic, validation, and output formatting
- **Existing modules**: filesystem.py, github.py, config.py, backup.py (not in scope)
- **Framework**: Click CLI with direct imports pattern
- **Error patterns**: "ERROR:" prefix with click.echo formatting

### Proposed Refactor Strategy
1. **Extract operation modules**: `operations.py` for business logic
2. **Extract common utilities**: `validation.py` and `output.py` for shared patterns
3. **Preserve CLI interface**: Keep main.py as thin command handlers
4. **Maintain imports**: Follow existing direct import patterns

### Risk Assessment
- **Low Risk**: Well-defined separation boundaries, comprehensive test coverage expected
- **Medium Risk**: Complex nested error handling patterns in original code
- **Mitigation**: Phase-by-phase validation with rollback capability

---

## Requirements Mapping

| Requirement | Tasks | Validation |
|------------|-------|------------|
| **FR-001** | CYCLE-002 | VAL-ACC-002 |
| **FR-002** | CYCLE-001 | VAL-ACC-004 |
| **FR-003** | CYCLE-003 | VAL-ACC-001 |
| **FR-004** | All cycles | VAL-ACC-001 |
| **FR-005** | All cycles | VAL-ACC-001 |

---

## Implementation Phases

### Phase 0: Environment & Setup

#### **ENV-001**: Validate Development Environment
**Dependencies**: None
**Prerequisites**: Development environment accessible
**Definition**: Confirm Python environment, uv tooling, and git repository state
**Validation**: All development commands run successfully
**Expected Result**: Clean development environment ready for refactoring

#### **ENV-002**: Setup Code Quality Tooling and Baseline Metrics
**Dependencies**: ENV-001
**Prerequisites**: Development environment validated
**Definition**: Configure and run black, ruff, pytest with coverage, measure current complexity
**Validation**: All quality tools run without errors, baseline metrics captured
**Expected Result**: Code quality toolchain functional, baseline metrics documented

#### **ENV-003**: Verify Dependencies and Test Framework
**Dependencies**: ENV-001
**Prerequisites**: Development environment validated
**Definition**: Run `uv sync --group dev`, verify all imports resolve, run existing tests
**Validation**: No dependency conflicts, all tests discoverable and runnable
**Expected Result**: All dependencies installed, test framework operational

### Phase 1: Baseline Validation

#### **VAL-BASE-001**: Run Full Existing Test Suite
**Dependencies**: Phase 0 complete
**Prerequisites**: All tooling setup completed
**Definition**: Execute `uv run pytest` and capture complete test results and coverage
**Validation**: All existing tests pass, no failures or errors
**Expected Result**: Baseline test state documented with 100% pass rate

#### **VAL-BASE-002**: Capture Baseline Code Quality Metrics
**Dependencies**: VAL-BASE-001
**Prerequisites**: Tests passing, quality tools available
**Definition**: Measure cyclomatic complexity, duplication percentage, line counts for main.py
**Validation**: Metrics collection successful, data recorded
**Expected Result**: Baseline metrics: main.py complexity, duplication, maintainability index

### Phase 2: Refactor Implementation (Validation Cycles)

#### **CYCLE-001**: Extract Common Patterns and Validation Logic (FR-002)
**Dependencies**: Phase 1 complete
**Prerequisites**: Baseline established
**Definition**: Create `validation.py` module extracting GitHub setup, repository validation, path validation patterns from main.py

**Tasks**:
- **VAL-001-1**: Run tests before extraction
- **IMPL-001-1**: Create `src/specli/validation.py` with extracted functions:
  - `validate_github_setup()` → returns setup info dict
  - `validate_source_repository(repo_url)` → returns validation dict
  - `validate_target_path(path)` → returns path validation dict
- **IMPL-001-2**: Update main.py imports and function calls to use validation module
- **VAL-001-2**: Run full test suite post-extraction

**Validation**: All tests pass, no behavioral changes, duplication metrics improve
**Expected Result**: Common validation patterns centralized, main.py reduced by ~50 lines

#### **CYCLE-002**: Separate CLI Handlers from Business Operations (FR-001)
**Dependencies**: CYCLE-001 complete
**Prerequisites**: Validation patterns extracted
**Definition**: Create `operations.py` module containing core business logic separated from CLI concerns

**Tasks**:
- **VAL-002-1**: Run tests before business logic extraction
- **IMPL-002-1**: Create `src/specli/operations.py` with business operations:
  - `deploy_claude_commands(source_repo, target_path, dry_run)` → returns operation result dict
  - `update_claude_commands(target_path, source_repo, dry_run, no_backup)` → returns operation result dict
- **IMPL-002-2**: Refactor main.py deploy/update commands to use operations module
- **VAL-002-2**: Run full test suite post-extraction

**Validation**: All tests pass, CLI commands are thin wrappers, business logic isolated
**Expected Result**: Main.py reduced to ~150 lines, business logic testable without Click mocking

#### **CYCLE-003**: Isolate Output Formatting and Messaging (FR-003)
**Dependencies**: CYCLE-002 complete
**Prerequisites**: Business logic extracted
**Definition**: Create `output.py` module for consistent message formatting and user feedback

**Tasks**:
- **VAL-003-1**: Run tests before output extraction
- **IMPL-003-1**: Create `src/specli/output.py` with formatting functions:
  - `format_error_message(error)` → formatted error string
  - `format_success_message(operation, details)` → formatted success string
  - `format_dry_run_message(action)` → formatted dry-run string
- **IMPL-003-2**: Update operations and main modules to use output formatting
- **VAL-003-2**: Run full test suite post-extraction

**Validation**: All tests pass, exact message formatting preserved, output logic centralized
**Expected Result**: Consistent output formatting, main.py further reduced, exact CLI output preserved

#### **CYCLE-004**: Final Integration and Cleanup
**Dependencies**: CYCLE-003 complete
**Prerequisites**: All extractions completed
**Definition**: Final cleanup, optimization, and integration validation

**Tasks**:
- **VAL-004-1**: Run comprehensive test suite
- **IMPL-004-1**: Remove any remaining duplication, optimize imports, add module docstrings
- **IMPL-004-2**: Verify all error handling paths preserved
- **VAL-004-2**: Run quality metrics comparison against baseline

**Validation**: All tests pass, metrics improved, no functionality changes
**Expected Result**: Clean, maintainable module structure with preserved functionality

### Phase 3: Integration Validation

#### **VAL-INT-001**: Run Comprehensive Regression Tests
**Dependencies**: Phase 2 complete
**Prerequisites**: All refactoring cycles completed
**Definition**: Execute full test suite including edge cases and error scenarios
**Validation**: 100% test pass rate, no regressions detected
**Expected Result**: Complete functional equivalence verified

#### **VAL-INT-002**: Validate CLI Behavior Preservation
**Dependencies**: VAL-INT-001
**Prerequisites**: Regression tests passing
**Definition**: Manual testing of all CLI commands with various argument combinations
**Validation**: Identical output messages, error handling, and exit codes
**Expected Result**: CLI interface completely unchanged

### Phase 4: Acceptance Validation

#### **VAL-ACC-001**: Validate Identical CLI Behavior (Acceptance Scenario 1)
**Covers**: Acceptance Scenario 1, FR-004, FR-005
**Dependencies**: Phase 3 complete
**Prerequisites**: Integration validation passed
**Definition**: Test `specli deploy <repo>` and `specli update` commands produce identical output
**Validation**: Output comparison with baseline behavior
**Expected Result**: Zero differences in CLI behavior

#### **VAL-ACC-002**: Validate Isolated Business Logic (Acceptance Scenario 2)
**Covers**: Acceptance Scenario 2, FR-001
**Dependencies**: VAL-ACC-001
**Prerequisites**: CLI behavior validated
**Definition**: Verify deployment/update logic can be modified in operations.py without touching CLI
**Validation**: Mock business logic change demonstrates isolation
**Expected Result**: Business logic changes isolated from CLI layer

#### **VAL-ACC-003**: Validate Testable Components (Acceptance Scenario 3)
**Covers**: Acceptance Scenario 3, FR-001
**Dependencies**: VAL-ACC-002
**Prerequisites**: Business logic isolation verified
**Definition**: Write unit tests for operations module without Click framework dependencies
**Validation**: Unit tests run independently of CLI framework
**Expected Result**: Business logic fully unit testable

#### **VAL-ACC-004**: Validate Reusable Patterns (Acceptance Scenario 4)
**Covers**: Acceptance Scenario 4, FR-002
**Dependencies**: VAL-ACC-003
**Prerequisites**: Component testability verified
**Definition**: Demonstrate validation and error handling patterns are reusable for new commands
**Validation**: Mock new command uses extracted patterns without duplication
**Expected Result**: Common patterns available for reuse

---

## Effort Estimation

| Phase | Tasks | Estimated Time | Dependencies |
|-------|-------|----------------|--------------|
| Phase 0 | 3 tasks | 1-2 hours | None |
| Phase 1 | 2 tasks | 1 hour | Phase 0 |
| Phase 2 | 4 cycles x 3-4 tasks | 6-8 hours | Phase 1 |
| Phase 3 | 2 tasks | 2-3 hours | Phase 2 |
| Phase 4 | 4 tasks | 2-3 hours | Phase 3 |
| **Total** | **19 tasks** | **12-17 hours** | Sequential |

---

## Success Metrics

### Quality Improvements Expected
- **Cyclomatic Complexity**: Reduce main.py complexity by 60%+
- **Code Duplication**: Eliminate duplication between deploy/update commands
- **Line Count**: Reduce main.py from 354 lines to ~100 lines
- **Testability**: Enable unit testing of business logic without CLI mocking

### Functional Preservation
- **Test Results**: 100% existing test pass rate maintained
- **CLI Output**: Zero differences in user-visible output
- **Error Handling**: All error scenarios preserve exact messages
- **Performance**: No degradation in command execution time

---

## Risk Mitigation

### Technical Risks
- **Complex error handling**: Incremental extraction with validation after each step
- **Output format changes**: Preserve exact click.echo calls and formatting
- **Import circular dependencies**: Carefully plan module dependencies

### Process Risks
- **Scope creep**: Strictly limit to main.py refactoring only
- **Over-engineering**: Focus on separation, not architectural overhaul
- **Test modifications**: Explicitly forbidden except for new unit tests

### Rollback Strategy
Each cycle includes pre/post validation - rollback to previous working state if any validation fails.