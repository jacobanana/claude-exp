# SPEC-001: Claude Command Deployer

## User Story

**As a** developer using Claude Code commands in my projects
**I want to** deploy and update my custom .claude commands to my current project or a specified path with a simple CLI tool
**So that** I can maintain consistency and share my Claude commands across projects without manual copying

## Problem & Context

**User Problem**: Developers create useful Claude Code commands but struggle to share and maintain them in their projects, leading to manual copying, version drift, and inconsistent tooling.

**Current Situation**: Users manually copy .claude folders to their project directories or recreate commands from scratch, making it difficult to keep commands updated and synchronized.

**Why This Matters**: Standardizing Claude commands in projects improves developer productivity and ensures consistent tooling workflows across development environments.

## Functional Requirements

- **FR-001**: System MUST provide a CLI tool that can deploy .claude commands from a source repository to the current working directory or a specified path
- **FR-002**: System MUST be able to clone/copy .claude folder contents to the target location (current directory or specified path)
- **FR-003**: System MUST support updating existing .claude commands in the target location
- **FR-004**: System MUST link to a GitHub repository as the source of truth for commands
- **FR-005**: System MUST be extremely lightweight with minimal dependencies
- **FR-006**: Users MUST be able to specify a target path for deployment, defaulting to current working directory if not specified
- **FR-007**: System MUST handle authentication for GitHub repository access using the Github CLI

## Acceptance Scenarios

1. **Given** a source repository with .claude commands, **When** I run the deploy command in a project directory, **Then** the .claude folder is copied to the current directory
2. **Given** a directory that already has .claude commands, **When** I run the update command, **Then** existing commands are updated with new versions from source
3. **Given** a specific target path, **When** I run the deploy command with --path option, **Then** commands are deployed to the specified path
4. **Given** the source repository is updated, **When** I run the update command, **Then** the target location receives the latest command versions
5. **Given** invalid repository access or missing .claude folder, **When** I run the tool, **Then** I receive a clear error message explaining the issue

## Success Criteria

**User Success**: Developers can deploy and maintain Claude commands to their projects in under 30 seconds with a single command

**Business Success**: Reduced time spent on manual command synchronization and improved consistency of Claude tooling in development environments

## Questions & Clarifications

**User Research Needed**:
- Do users prefer deployment to current directory or need to specify paths?
    Default to current directory, with --path option for specific locations
- What's the preferred authentication method for GitHub access?
    Using the Github CLI
- Do users need selective command deployment or always full .claude folder sync?
    To keep things simple, it will be a full sync.

**Business Decisions Required**:
- Should this tool support other Git providers besides GitHub?
    Just github for now
- What's the installation/distribution method (npm, binary, script)?
    NPM

**Assumptions to Validate**:
- Users work primarily from project directories where they want .claude commands deployed
    Yes
- Source repository .claude folder structure is standardized
    Yes
- Users prefer command-line interface over GUI tool
    Yes