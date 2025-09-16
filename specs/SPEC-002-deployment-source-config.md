# SPEC-002: Deployment Source Configuration

## User Story

**As a** developer using the Claude command deployer
**I want to** save the source repository configuration locally so I don't need to specify it every time I update
**So that** I can quickly update my commands with a simple `update` command without remembering repository details

## Problem & Context

**User Problem**: Developers need to remember and re-enter the source repository URL every time they want to update their deployed Claude commands, making updates cumbersome and error-prone.

**Current Situation**: Users must manually specify the source repository each time they run the update command, leading to typing errors and friction in the update process.

**Why This Matters**: Reducing friction in the update process encourages developers to keep their Claude commands current and improves the overall developer experience.

## Functional Requirements

- **FR-001**: System MUST create a configuration file when deploying commands that remembers the source repository
- **FR-002**: System MUST read the configuration file during update operations to automatically determine the source repository
- **FR-003**: System MUST allow the update command to work without specifying a repository when configuration exists
- **FR-004**: System MUST store the configuration file in the same location where commands are deployed
- **FR-005**: Users MUST be able to override the saved repository by explicitly providing a new source during update

## Acceptance Scenarios

1. **Given** I deploy commands from a repository for the first time, **When** the deployment completes, **Then** a configuration file is created storing the source repository information
2. **Given** a configuration file exists with source repository info, **When** I run the update command without specifying a repository, **Then** the system uses the saved repository to update commands
3. **Given** a configuration file exists, **When** I run the update command with a different repository specified, **Then** the system uses the new repository and updates the configuration file
4. **Given** no configuration file exists, **When** I run the update command without specifying a repository, **Then** I receive a clear error message asking me to specify the source repository
5. **Given** a configuration file exists but the saved repository is no longer accessible, **When** I run the update command, **Then** I receive a clear error message about the repository access issue

## Success Criteria

**User Success**: Developers can update their deployed commands with zero additional input after the initial deployment

**Business Success**: Increased frequency of command updates due to reduced friction in the update process

## Questions & Clarifications

**User Research Needed**:
- What information should be stored beyond just the repository URL?
    The repo URL and optional version, tag or branch
- Should the config file be human-readable/editable?
    Yes

**Business Decisions Required**:
- Should the configuration file be ignored by git by default?
    No, that should be committed.
- What should the configuration file be named and what format should it use?
    specli.settings.json

**Assumptions to Validate**:
- Users primarily update from the same source repository they initially deployed from
    Yes
- Configuration should be stored locally in the deployment target directory
    Yes
- Simple key-value configuration is sufficient for this use case
    Yes