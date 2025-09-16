# Implementation Plan: Deployment Source Configuration

## Progress Tracking
**Instructions for Claude Code**: Before starting any task, you MUST:
1. Verify all prerequisites are marked as ✅ COMPLETE
2. Update task status to 🔄 IN PROGRESS when starting
3. Update task status to ✅ COMPLETE when finished
4. Validate all task requirements before marking complete

## Specification Summary
Implementing configuration file persistence for source repository information in the specli CLI tool. When commands are deployed, the source repository will be saved to `specli.settings.json` in the target directory. The update command will read this configuration to automatically determine the source repository, eliminating the need for users to re-specify it on each update.

## Technical Approach Validation
**Current Architecture**: The CLI uses Click for command handling, with separate modules for filesystem operations (`filesystem.py`) and GitHub operations (`github.py`). The current `deploy` and `update` commands work with temporary directories and manual source specification.

**Proposed Integration**:
- Add a new `config.py` module to handle configuration file operations
- Modify `deploy` command to save source repository info to `specli.settings.json`
- Modify `update` command to read from configuration file when no `--source` is provided
- Use JSON format as specified in the business requirements

**Technology Validation**: ✅ Approved
- JSON format aligns with Python's built-in `json` module
- File-based configuration is simple and meets the human-readable requirement
- Integration with existing Click CLI structure is straightforward

## Requirements Mapping
| Requirement | Task Coverage |
|-------------|---------------|
| FR-001: Create config file on deploy | TEST-2A1, IMPL-2A1 |
| FR-002: Read config during update | TEST-2B1, IMPL-2B1 |
| FR-003: Update without specifying repo | TEST-2B1, IMPL-2B1 |
| FR-004: Store in deployment location | TEST-2A1, IMPL-2A1 |
| FR-005: Override saved repository | TEST-2C1, IMPL-2C1 |

## Implementation Phases

### Phase 0: Environment & Setup ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: None
**All tasks can run in parallel**

- [ ] **ENV-001**: Verify existing test framework setup
  - **Status**: ⬜ NOT STARTED
  - **Definition**: Ensure pytest and existing test structure can handle new configuration tests
  - **Validation**: Run `pytest --version` and verify existing tests pass

- [ ] **ENV-002**: Verify JSON module availability
  - **Status**: ⬜ NOT STARTED
  - **Definition**: Confirm Python's built-in JSON module is available (no additional dependencies needed)
  - **Validation**: Import json in Python and verify functionality

### Phase 1: Initial Test Structure ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 0 ✅ COMPLETE
**TDD Rule**: Create failing tests for core configuration structure only

- [ ] **TEST-001**: Write failing tests for configuration module structure
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 0 ✅ COMPLETE
  - **Covers**: Basic structure for configuration operations
  - **Definition**: Create test file `test_config.py` with tests for config module interface (save_config, load_config functions)
  - **Expected Result**: Tests MUST fail (Red phase) - module and functions don't exist yet
  - **Validation**: Run `pytest tests/test_config.py -v` - all tests should fail with import/attribute errors

- [ ] **IMPL-001**: Implement minimal configuration module structure
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-001 ✅ COMPLETE (and failing)
  - **Covers**: Basic scaffolding for config operations
  - **Definition**: Create `src/specli/config.py` with empty save_config() and load_config() functions that return placeholder values
  - **Expected Result**: Phase 1 tests pass, no actual functionality yet
  - **Validation**: Run `pytest tests/test_config.py -v` - imports should work, basic structure tests pass

### Phase 2: Feature Implementation (TDD Cycles) ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 1 ✅ COMPLETE

#### TDD Cycle 2A: Configuration File Creation ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED

- [ ] **TEST-2A1**: Write failing test for saving configuration on deploy
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 1 ✅ COMPLETE
  - **Covers**: FR-001, FR-004 - Create config file with repository info in deployment location
  - **Definition**: Write test that calls save_config() and verifies `specli.settings.json` is created with correct repository URL and optional branch/tag
  - **Expected Result**: Test MUST fail - save_config() doesn't create actual files yet
  - **Validation**: Run test - should fail because no JSON file is created

- [ ] **IMPL-2A1**: Implement configuration file saving
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2A1 ✅ COMPLETE (and failing)
  - **Covers**: FR-001, FR-004 implementation
  - **Definition**: Implement save_config() to create `specli.settings.json` with repository URL, optional branch/tag, and timestamp
  - **Expected Result**: TEST-2A1 passes, configuration file is created correctly
  - **Validation**: Run TEST-2A1 - must pass, verify JSON file contains expected structure

- [ ] **REFACTOR-2A1**: Refactor configuration saving if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2A1 ✅ COMPLETE (all tests passing)
  - **Definition**: Improve code structure, error handling, or performance without changing behavior
  - **Expected Result**: Code improved, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

#### TDD Cycle 2B: Configuration File Reading ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 2A ✅ COMPLETE

- [ ] **TEST-2B1**: Write failing test for reading configuration during update
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 2A ✅ COMPLETE
  - **Covers**: FR-002, FR-003 - Read config file and use repository info for updates
  - **Definition**: Write test that creates a config file, calls load_config(), and verifies correct repository info is returned
  - **Expected Result**: Test MUST fail - load_config() doesn't read actual files yet
  - **Validation**: Run test - should fail because load_config() returns placeholder data

- [ ] **IMPL-2B1**: Implement configuration file reading
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2B1 ✅ COMPLETE (and failing)
  - **Covers**: FR-002, FR-003 implementation
  - **Definition**: Implement load_config() to read `specli.settings.json` and return repository configuration data
  - **Expected Result**: TEST-2B1 passes, configuration data is read correctly
  - **Validation**: Run TEST-2B1 - must pass, verify correct data is loaded from JSON

- [ ] **REFACTOR-2B1**: Refactor configuration reading if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2B1 ✅ COMPLETE (all tests passing)
  - **Definition**: Improve error handling for missing/corrupted config files
  - **Expected Result**: Better error handling, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

#### TDD Cycle 2C: Repository Override Functionality ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 2B ✅ COMPLETE

- [ ] **TEST-2C1**: Write failing test for repository override during update
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 2B ✅ COMPLETE
  - **Covers**: FR-005 - Override saved repository with new source and update config
  - **Definition**: Write test that loads existing config, provides different repository source, and verifies new source is used and config is updated
  - **Expected Result**: Test MUST fail - override functionality doesn't exist yet
  - **Validation**: Run test - should fail because config isn't updated with new source

- [ ] **IMPL-2C1**: Implement repository override functionality
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-2C1 ✅ COMPLETE (and failing)
  - **Covers**: FR-005 implementation
  - **Definition**: Modify config handling to prioritize explicitly provided source and update config file with new source
  - **Expected Result**: TEST-2C1 passes, config file is updated when override source is provided
  - **Validation**: Run TEST-2C1 - must pass, verify config file contains new repository info

- [ ] **REFACTOR-2C1**: Refactor override functionality if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-2C1 ✅ COMPLETE (all tests passing)
  - **Definition**: Optimize configuration update logic and ensure clean separation of concerns
  - **Expected Result**: Cleaner code structure, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

### Phase 3: CLI Integration (TDD Cycles) ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 2 ✅ COMPLETE

#### TDD Cycle 3A: Deploy Command Integration ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED

- [ ] **TEST-3A1**: Write failing integration test for deploy command saving config
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 2 ✅ COMPLETE
  - **Covers**: Integration of config saving into deploy command
  - **Definition**: Write CLI integration test that runs deploy command and verifies `specli.settings.json` is created in target directory
  - **Expected Result**: Test MUST fail - deploy command doesn't save config yet
  - **Validation**: Run integration test - should fail because deploy doesn't create config file

- [ ] **IMPL-3A1**: Integrate config saving into deploy command
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-3A1 ✅ COMPLETE (and failing)
  - **Covers**: Modify deploy command to call save_config() after successful deployment
  - **Definition**: Update deploy() function in main.py to save repository configuration after successful .claude folder deployment
  - **Expected Result**: TEST-3A1 passes, deploy command creates configuration file
  - **Validation**: Run integration test - must pass, verify deploy creates config file

#### TDD Cycle 3B: Update Command Integration ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Prerequisites**: TDD Cycle 3A ✅ COMPLETE

- [ ] **TEST-3B1**: Write failing integration test for update command reading config
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TDD Cycle 3A ✅ COMPLETE
  - **Covers**: Integration of config reading into update command
  - **Definition**: Write CLI integration test that creates config file, runs update command without --source, and verifies it uses config repository
  - **Expected Result**: Test MUST fail - update command doesn't read config yet
  - **Validation**: Run integration test - should fail because update still prompts for source

- [ ] **IMPL-3B1**: Integrate config reading into update command
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: TEST-3B1 ✅ COMPLETE (and failing)
  - **Covers**: Modify update command to load and use saved repository configuration
  - **Definition**: Update update() function in main.py to load config and use saved repository when --source is not provided
  - **Expected Result**: TEST-3B1 passes, update command uses saved configuration
  - **Validation**: Run integration test - must pass, verify update uses config without prompting

- [ ] **REFACTOR-3B1**: Refactor CLI integration if needed
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: IMPL-3B1 ✅ COMPLETE (all tests passing)
  - **Definition**: Clean up command logic and improve error messages for config-related operations
  - **Expected Result**: Cleaner CLI code, better user messages, all tests still pass
  - **Validation**: Run full test suite - all tests still pass

### Phase 4: Acceptance Validation ⬜ NOT STARTED
**Status**: ⬜ NOT STARTED
**Dependencies**: Phase 3 ✅ COMPLETE

- [ ] **VAL-001**: Validate scenario 1 - Config file created on deploy
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: Phase 3 ✅ COMPLETE
  - **Covers**: Given I deploy commands from a repository for the first time, When the deployment completes, Then a configuration file is created storing the source repository information
  - **Definition**: Run end-to-end test deploying from a test repository and verify `specli.settings.json` is created with correct content
  - **Validation**: Manual verification that config file exists and contains repository URL and metadata

- [ ] **VAL-002**: Validate scenario 2 - Update uses saved config
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-001 ✅ COMPLETE
  - **Covers**: Given a configuration file exists with source repository info, When I run the update command without specifying a repository, Then the system uses the saved repository to update commands
  - **Definition**: Create config file manually, run update command without --source, verify it uses saved repository
  - **Validation**: Manual verification that update command reads config and uses saved repository URL

- [ ] **VAL-003**: Validate scenario 3 - Repository override updates config
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-002 ✅ COMPLETE
  - **Covers**: Given a configuration file exists, When I run the update command with a different repository specified, Then the system uses the new repository and updates the configuration file
  - **Definition**: Create config with one repository, run update with different --source, verify new repository is used and config is updated
  - **Validation**: Manual verification that config file is updated with new repository information

- [ ] **VAL-004**: Validate scenario 4 - Error when no config exists
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-003 ✅ COMPLETE
  - **Covers**: Given no configuration file exists, When I run the update command without specifying a repository, Then I receive a clear error message asking me to specify the source repository
  - **Definition**: Remove config file, run update without --source, verify clear error message
  - **Validation**: Manual verification that appropriate error message is displayed

- [ ] **VAL-005**: Validate scenario 5 - Error when saved repository is inaccessible
  - **Status**: ⬜ NOT STARTED
  - **Prerequisites**: VAL-004 ✅ COMPLETE
  - **Covers**: Given a configuration file exists but the saved repository is no longer accessible, When I run the update command, Then I receive a clear error message about the repository access issue
  - **Definition**: Create config with invalid/inaccessible repository, run update, verify clear error message
  - **Validation**: Manual verification that repository access error is properly reported

## Task Status Legend
- ⬜ NOT STARTED: Task not yet begun
- 🔄 IN PROGRESS: Currently working on task
- ✅ COMPLETE: Task finished and validated
- ❌ BLOCKED: Cannot proceed due to failed prerequisites

## Progress Summary
**Total Tasks**: 21
**Completed**: 0 ✅
**In Progress**: 0 🔄
**Remaining**: 21 ⬜
**Blocked**: 0 ❌

## Risk Assessment
**Technical Risks**:
- **JSON file corruption**: Mitigated by proper error handling and validation in load_config()
- **File permissions**: Config file creation might fail in restricted directories - error handling needed
- **Concurrent access**: Multiple CLI instances could conflict - acceptable risk for single-user CLI tool

**Integration Risks**:
- **CLI command complexity**: Adding config logic to existing commands - mitigated by keeping config operations isolated in separate module
- **Backward compatibility**: Existing usage should continue working - existing prompts preserved as fallback

## Effort Estimation
**Development Time**: 2-3 days
- **Phase 0-1**: 2-3 hours (setup and basic structure)
- **Phase 2**: 6-8 hours (core configuration functionality)
- **Phase 3**: 4-6 hours (CLI integration)
- **Phase 4**: 2-3 hours (acceptance validation)

**Testing Coverage**: All functional requirements covered with unit tests, integration tests, and manual acceptance validation.