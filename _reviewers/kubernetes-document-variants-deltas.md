---
title: Document Variants Deltas
description: 'When introducing new code-path variants (e.g., “ForResize” vs base algorithms),
  comments/documentation must clearly explain:


  1) **The delta vs the base implementation**: what changes and what stays identical.'
repository: kUbernetes/kUbernetes
label: Documentation
language: Go
comments_count: 7
repository_stars: 128688
---

When introducing new code-path variants (e.g., “ForResize” vs base algorithms), comments/documentation must clearly explain:

1) **The delta vs the base implementation**: what changes and what stays identical.
2) **The rationale for separate variants** (“why”) so future refactoring can safely unify or change behavior.
3) **The key algorithmic scheme** (e.g., any partitionA/partitionB split) recorded once in a durable overview—then only minimal per-function notes for true differences.
4) **Comment stability/quality**: avoid copy-paste reiteration of base behavior, and avoid PR-specific phrasing like “This PR…”. Replace with stable TODOs or tracking-issue links.

Practical checklist:
- At the top of each new variant entry point, add a short line such as:
  ```go
  // Delta vs takeByTopologyNUMADistributed: ForResize changes allocation/accounting to retain existing CPUs; overall NUMA selection & balance scoring are otherwise identical.
  ```
- Add one cumulative block for the whole variant family (e.g., all `*ForResize` functions) that explains the scheme once (split/partitioning + what feeds what).
- Remove/shorten comments that merely restate base behavior; keep only what differs.
- If the comment references the PR/release context, convert it to a stable TODO (and link to a tracking issue).

This prevents duplicated/AI-like narrative comments and ensures the codebase contains durable, maintainable documentation of “what changed” and “why it exists.”