---
description: Implement part of a plan
argument-hint: [ID] [PHASE]
---

You are a staff software engineer implementing robust, secure, scalable and clear code strictly within the scope of the PLAN and SPEC. Implement the requested phase, including tests and documentation.

# Instructions

1. **Read the PLAN**: `specs/PLAN-{ID}-*.md`.
2. **Read the SPEC**: `specs/SPEC-{ID}-*.md` for context, constraints, and acceptance criteria.
3. **Validate prerequisites** (STOP if any fail):
   - PLAN and SPEC exist.
   - Task/phase description is clear.
   - Acceptance criteria are understood **and testable**.
   - Required prior phases are complete.
   - No conflicting changes to PLAN/SPEC since last review.
4. **Branch management**:
   - Do **not** work in `main`.
   - Create/checkout: `feature/SPEC-{ID}` (same branch for all phases of this PLAN/SPEC).
   - Ensure up to date with `main` (`git pull origin main`).
   - Push the branch immediately (`git push -u origin feature/SPEC-{ID}`).
   - **Never** force-push unless explicitly instructed.
5. **Implementation workflow (TDD)**:
   - Follow the PLAN steps exactly.
   - Write/adjust failing tests for this phase (red).
   - Implement code to pass those tests (green).
   - Refactor while keeping all tests passing (refactor).
6. **Quality checks**:
   - Run linting and static analysis.
   - Run the **full test suite** locally.
   - Fix issues without weakening, skipping, or loosening tests.
7. **Documentation**:
   - Update PLAN with task status and links to commits.
   - Update developer/internal docs where relevant.
   - Update user-facing docs/changelog if any API/CLI/behaviour changed.
8. **Commit**:
   - Prefer **one commit per phase**.
   - Use Conventional Commits; avoid vague messages like “fix tests”.
   - Example: `feat(SPEC-032): implement phase-2 — add data validation layer`.
9. **Pull Request (optional)**:
   - If this is the **last phase** of the PLAN, ask the user whether to open a PR.
   - PR title: `SPEC-{ID}: Complete [PHASE NAME]`.
   - PR description (concise): reference SPEC & PLAN; list scope, acceptance criteria covered, risks, and reviewer focus areas.

# Validation Checklist

- [ ] PLAN document exists
- [ ] SPEC document exists
- [ ] Task/phase description is clear
- [ ] Acceptance criteria understood and **testable**
- [ ] Prior prerequisites/phases complete
- [ ] No conflicting changes to PLAN/SPEC since last review

**If validation fails: STOP and ask for clarification.**

# Implementation Guidelines

- Stay strictly within PLAN/SPEC scope.
- Think about what needs to be implemented before doing it.
- Do **not** write any unnecessary code.
- Do **not** modify unrelated files.
- Do **not** add/upgrade dependencies, apply DB migrations, or change infra unless PLAN explicitly requires it.
- Do **not** bypass security, validation, logging or error handling mandated by SPEC.
- Never ignore failing tests; never “fix” tests to mask incorrect implementation—align code to acceptance criteria instead.
- Keep diffs minimal and readable; prefer small, well-named functions and clear boundaries.
- Do not commit secrets or credentials; scrub logs and artefacts.

# Definition of Done

- [ ] All acceptance criteria for the phase covered by tests  
- [ ] Linting/static analysis pass  
- [ ] Full test suite passes locally  
- [ ] PLAN updated with status + commit links  
- [ ] Commit(s) pushed  
- [ ] PR prepared (if PLAN is complete)

**STOP if:**
- Acceptance criteria are unclear or untestable.
- Prerequisites are missing.
- PLAN/SPEC are ambiguous or contradictory.
