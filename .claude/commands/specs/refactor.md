---
description: Prepare a developer-driven specification for a non-functional refactor
argument-hint: [details of refactoring]
---

# Prepare Refactor Spec

You are a **staff developer** with deep knowledge of this codebase. Produce a **concise, decision-ready specification** for a **non-functional refactor** that improves **best practices, scalability, reusability, security**, and **reduces technical debt and complexity**. This spec is for developer stakeholders; **implementation planning comes later**.

## Variables

SPEC_NAME: short slug derived from description to be used as a reference
SPEC_NUMBER: incremental number for files in the SPEC folder (eg: 001, 002, 003, ...)

## Behaviour

1. **Parse Input**
   - Extract the refactor target [what part of the codebase is being refactored].
   - If the input spans multiple unrelated areas, **ask to split into separate specs and STOP**.

2. **Hard Constraints**
   - **No functionality change**: external behaviour and user-visible outputs remain identical.
   - **No changes to tests**: do not alter functional tests.
   - **Backwards-compatible public interfaces** unless explicitly stated otherwise.
   - **Data/contracts unchanged** unless explicitly stated otherwise.

3. **Ambiguity Handling**
   - For anything unclear, add a bullet under **Questions & Clarifications** with the tag **[NEEDS CLARIFICATION]**.

4. **Keep It Non-Implementation**
   - Describe **WHAT** will be true after the refactor, not **HOW** to implement it.

5. **Acceptance Style**
   - All acceptance criteria must use **Given / When / Then**.

6. **Output**
   - Produce **Markdown only**, following the structure below.

---

## Output — Markdown Template

# Refactor Spec — [Concise Title]

## 1. User Story (Single, focused story)
- **As a** [user type]  
- **I want to** [specific refactor goal]  
- **So that** [clear benefit/value]  

## 2. Problem & Context
- **Developer Problem:** [pain point this addresses]  
- **Current Situation:** [how it is currently handled]  
- **Why This Matters Now:** [reason this is important to address now]  

## 3. Refactoring Requirements (Must-haves only)
- **FR-001:** System MUST [requirement]  
- **FR-002:** System MUST [requirement]  
- **FR-003:** System MUST [requirement]  
- **FR-004:** System MUST [requirement] **[NEEDS CLARIFICATION]**  

## 4. Acceptance Scenarios (Given / When / Then)
1. **Given** [initial state], **When** [action], **Then** [expected outcome]  
2. **Given** [initial state], **When** [action], **Then** [expected outcome]  
3. **Given** [initial state], **When** [action], **Then** [expected outcome]  

## 5. Success Criteria
- **User Success:** How will we know [users/developers] can achieve their goal after the refactor?  
- **Business Success:** What measurable business outcome should improve (e.g. [maintainability, speed, risk reduction])?  

## 6. Scope Boundaries
- **In Scope:** [high-level modules/files to refactor]  
- **Out of Scope:** [what is explicitly not included]  

## 7. Risks & Mitigations
- **Risk:** [potential risk] → **Mitigation:** [strategy]  
- **Risk:** [potential risk] → **Mitigation:** [strategy]  

## 8. Questions & Clarifications
- [Unclear requirement] **[NEEDS CLARIFICATION]**  
- [Business decision needed] **[NEEDS CLARIFICATION]**  
- [Assumption to validate]  


# Output Format:

Save as "specs/SPEC-{SPEC_NUMBER}-{SPEC_NAME}.md" in the root directory. If this file already exists, integrate the new requirements with existing content, clearly marking new additions.
