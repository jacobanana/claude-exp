# SPEC-004: CLI Architecture Refactor

## User Story

**As a** developer working on the specli codebase
**I want** the CLI commands to be separated from business logic
**So that** I can easily test, maintain, and extend the application

## Problem & Context

**Developer Problem**: The current `main.py` file contains 300+ lines mixing CLI presentation logic with core business operations, making the codebase difficult to test and maintain.

**Current Situation**:
- Business logic is embedded within Click command functions
- Functions are 150+ lines long with mixed responsibilities
- Unit testing requires mocking CLI interactions
- Code duplication exists between deploy and update operations

**Why This Matters**: As the application grows, this architecture will slow development velocity and increase bug risk. Clean separation enables independent testing of business logic and easier feature additions.

## Functional Requirements

**FR-001**: CLI commands MUST delegate core operations to separate business logic modules
**FR-002**: Business logic functions MUST be testable without CLI dependencies
**FR-003**: Common operations MUST be extracted to eliminate code duplication
**FR-004**: CLI layer MUST handle only presentation, user input, and output formatting
**FR-005**: Existing user-facing behavior MUST remain unchanged after refactor

## Acceptance Scenarios

1. **Given** the refactored codebase, **When** a developer runs unit tests on business logic, **Then** tests execute without requiring CLI mocking
2. **Given** the new architecture, **When** a developer adds a new operation, **Then** they can implement and test business logic independently of CLI concerns
3. **Given** the refactored code, **When** users run deploy and update commands, **Then** all existing functionality works identically to before
4. **Given** separated concerns, **When** a developer needs to modify error handling, **Then** they can update it in one place rather than multiple CLI functions
5. **Given** the new structure, **When** a developer reviews the main.py file, **Then** each CLI command function is under 50 lines and focuses only on user interaction

## Success Criteria

**Developer Success**:
- Business logic can be unit tested without CLI dependencies
- Main CLI command functions are under 50 lines each
- Common operations are centralized and reusable

**Code Quality Success**:
- Reduced cyclomatic complexity in CLI functions
- Clear separation between presentation and business layers
- Eliminated code duplication between commands

## Questions & Clarifications

**Architecture Decisions Required**:
- Should business logic go in `operations.py`, `commands.py`, or `core.py`?
- How should we handle shared state between operations?
- Should CLI utilities be in a separate module or part of main?

**Testing Strategy Needed**:
- What level of test coverage should we maintain during refactor?
- Should we add integration tests to verify CLI behavior preservation?

**Implementation Approach**:
- Should this be done incrementally (one command at a time) or all at once?
- How do we ensure no behavioral regressions during refactor?