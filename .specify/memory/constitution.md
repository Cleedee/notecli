<!--
SYNC IMPACT REPORT
==================
Version change: (none) → 1.0.0 (initial constitution)
Modified principles: (none) — first creation
Added sections:
  - Core Principles (5 principles): CLI-First, Test-Driven, Entity-Driven Design,
    Observability & Debuggability, Simplicity & YAGNI
  - Additional Constraints (tech stack, dependency policy, code quality)
  - Development Workflow (PR requirements, testing gates, commit discipline)
  - Governance (amendment procedure, versioning policy, compliance review)
Templates requiring updates:
  - .specify/templates/plan-template.md       ✅ no changes needed (generic Constitution Check section)
  - .specify/templates/spec-template.md        ✅ no changes needed (technology-agnostic)
  - .specify/templates/tasks-template.md       ✅ no changes needed (generic structure)
  - .specify/templates/commands/*.md           ✅ no command files present
  - README.md                                  ✅ no constitution references to update
Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Original adoption date unknown; set to project creation date as best estimate.
-->

# NOTECLI Constitution

## Core Principles

### I. CLI-First

Every feature MUST be usable from the command line; the CLI is the primary
interface for all user interactions. New capabilities MUST be accessible via
`notecli` subcommands with clear help text, sensible defaults, and human-readable
output. Programmatic APIs (library modules) are secondary and exist to support
the CLI or future integrations.

**Rationale**: NoteCLI is a CLI tool first — usability from the terminal is the
core value proposition.

### II. Test-Driven (NON-NEGOTIABLE)

All production code MUST be developed using Test-Driven Development: tests are
written before implementation, must fail initially, and only then is
implementation permitted. The Red-Green-Refactor cycle is strictly enforced.
Every module, service, and entity MUST have corresponding unit tests.

**Rationale**: Tests are the safety net that enables confident refactoring and
feature addition without regressions.

### III. Entity-Driven Design

Domain entities (e.g., characters, items, tables, dice rolls) MUST be defined as
explicit, self-contained data structures in `src/notecli/entities/`. Each entity
MUST be independently documented and testable. Business logic MUST operate on
these entities through pure functions whenever possible.

**Rationale**: Clear entity boundaries make the codebase predictable, testable,
and easier to extend when adding AI-driven features.

### IV. Observability & Debuggability

All user-facing commands MUST produce clear, structured output. Errors MUST be
written to stderr with actionable messages. When the AI agent (`agno`) is
integrated, interactions MUST be logged in a structured format (JSON or
key-value pairs) to enable replay and debugging.

**Rationale**: Debuggability is essential for a game-assistance tool where users
need to understand why a decision or roll produced a given result.

### V. Simplicity & YAGNI

Start simple. Do NOT add abstractions, patterns, or dependencies unless there is
a concrete, current use case that demands them. Avoid premature optimization.
Each new dependency MUST be justified by a specific feature need that cannot be
met with the standard library or existing dependencies.

**Rationale**: Keeping the codebase minimal reduces maintenance burden and
accelerates iteration during the early development phase.

## Additional Constraints

### Technology Stack

- **Language**: Python 3.14+ (as specified in `pyproject.toml`)
- **Package Manager**: `uv` (via `uv_build` backend)
- **Entry Point**: `notecli` → `notecli.main:main`
- **AI Dependency**: `agno` — used exclusively for AI-assisted gameplay features

### Dependency Policy

- New dependencies MUST be added to `pyproject.toml` with version constraints.
- Each dependency addition requires a brief justification in the commit message.
- Lock file (`uv.lock`) MUST be committed and kept in sync after any dependency
  change.

### Code Quality

- All modules MUST be importable without side effects.
- The `src/notecli/` package structure MUST be respected: entities in
  `entities/`, services in dedicated modules, CLI logic in `main.py` or
  subcommand modules.
- No code in `__init__.py` beyond package-level exports.

## Development Workflow

### Pull Requests & Reviews

- All changes to `main` MUST go through a pull request (PR).
- PRs MUST include: a clear description, linked issue/spec if applicable, and
  test results showing all gates pass.
- At least one review MUST verify compliance with this constitution before merge.

### Testing Gates

- No code merges without passing tests (`pytest` or equivalent).
- New features MUST include tests before merge.
- Breaking changes to existing entity contracts MUST include migration tests.

### Commit Discipline

- Commits MUST be atomic: one logical change per commit.
- Commit messages MUST follow conventional commits format (e.g.,
  `feat:`, `fix:`, `test:`, `docs:`, `refactor:`).
- The lock file MUST be updated in the same commit as any `pyproject.toml`
  dependency change.

## Governance

This constitution supersedes all other development practices in the NoteCLI
repository. Amendments to this document require:

1. **Proposal**: The amender drafts changes and produces a Sync Impact Report
   (prepending an HTML comment to this file).
2. **Review**: Changes are reviewed for consistency with project goals and
   existing principles.
3. **Approval**: At least one project maintainer must approve the amendment.
4. **Migration**: If the amendment introduces breaking changes to workflows, a
   migration plan must be documented.

### Versioning Policy

The constitution version follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Backward-incompatible principle removals or redefinitions.
- **MINOR**: New principles added or existing principles materially expanded.
- **PATCH**: Clarifications, wording improvements, typo fixes.

### Compliance Review

All PRs and reviews MUST verify constitution compliance. Violations must be
documented in the PR's Complexity Tracking section (see plan template) with
justification for why the simpler approach was insufficient.

**Version**: 1.0.0 | **Ratified**: 2026-04-04 | **Last Amended**: 2026-04-04
