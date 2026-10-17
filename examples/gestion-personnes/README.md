# Historical Spring Boot workflow case study

Source project: [gestion-personnes](https://github.com/jordankeyanfe586/gestion-personnes). This page summarizes a historical qualification report, not a new execution.

## Problem and scope
In a disposable clone, updating an inactive person through PUT rebuilt the entity with its active flag set to true. The task was restricted to preserving the original status in the service and adding regression coverage, without a controller/DTO refactor. A separate pre-existing documentation edit had to remain outside the change.

## Roles and sequence
The historical report attributes implementation to Claude Code and independent review to Antigravity. The user approved sensitive Git operations separately. The sequence covered initial Git inspection, scope definition, a service fix, two unit tests and one integration test, verification, separate review and local integration. A native compaction/resumption scenario was also documented before committing.

## Reported outcome
The private qualification report records failing inactive-person scenarios before correction, then `./mvnw clean package` with 26 tests and no failures. It records a separate review and human approvals before staging, commit, integration and branch deletion. Those results concern the disposable clone; they are not claimed as tests run on this public edition or on today's Java repository.

## Evidence limits
The [anonymized qualification report](../../tests/claude/REQUALIFICATION.md) retains the detailed historical account. The original temporary clone, raw reports and review traces are no longer available at their recorded locations. Private commit identifiers are not part of this edition's Git history. The scenario was not recreated to manufacture missing evidence, and the Java source repository was not modified during preparation.

The case illustrates AI-assisted development with human oversight. It does not establish that the owner personally implemented every change or that the current provider versions are fully requalified.
