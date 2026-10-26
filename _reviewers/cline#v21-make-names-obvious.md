---
title: Make Names Obvious
description: 'When adding or renaming identifiers in code or telemetry, ensure the
  name communicates meaning, matches existing conventions, and is hard to misuse.


  Apply this checklist:'
repository: cline/cline#v21
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When adding or renaming identifiers in code or telemetry, ensure the name communicates meaning, matches existing conventions, and is hard to misuse.

Apply this checklist:
1) Prefer intention-revealing names
- Avoid vague flags and “negation-based” semantics.
- Prefer positive, state-describing names (or enums) over booleans that require explanation.

2) Use existing naming standards/types
- Reuse shared types/constants for domain identifiers when they exist (e.g., a `ClientName` union/type instead of ad-hoc strings).
- Follow established casing rules that depend on key origin/surface (e.g., context/caller-supplied keys vs envelope/global enrichment keys).

3) Keep schemas consistent across call sites
- If you rename an event/helper parameter/property (e.g., `taskId` → `ulid`), update all call sites; positional arguments won’t be caught by TS, so semantic drift can slip in.

4) Make public APIs discoverable
- If multiple functions could be called, ensure the primary one is obvious (or rename/comment so there’s no guesswork which one to use).

Example (avoid boolean/negation + use state names):
```ts
// Prefer this:
type PromptSeedStatus = 'seeded' | 'written'

interface Ctx {
  promptSeedStatus?: PromptSeedStatus
}

// Over this vague/negation-prone approach:
interface Ctx {
  promptSeeded?: boolean // meaning of false is not named
}
```