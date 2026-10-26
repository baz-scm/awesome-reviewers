---
title: Meaningful Identifier Naming
description: 'Use names that encode intent and state, align identifiers with shared
  types, and keep renamed external keys consistent.


  Apply this checklist:

  - **Prefer shared typed identifiers**: If there’s a canonical type like `ClientName`,
  reuse it for client identifiers; don’t fall back to loose `string` escape hatches—extend
  the shared type to include missing...'
repository: cline/cline#v26
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 70893
---

Use names that encode intent and state, align identifiers with shared types, and keep renamed external keys consistent.

Apply this checklist:
- **Prefer shared typed identifiers**: If there’s a canonical type like `ClientName`, reuse it for client identifiers; don’t fall back to loose `string` escape hatches—extend the shared type to include missing variants.
- **Avoid vague booleans**: If a flag name is unclear (or you end up writing negations like `!background`), rename it to express the positive intent (e.g., `userInitiated`).
- **Model multi-state domains explicitly**: If a boolean actually represents multiple real states (e.g., “prompt seeded vs prompt provided”), use a string/enum field (e.g., `entry: 'run' | 'continue'`, `promptSource: 'seeded' | 'written'`) rather than `true/false`.
- **Make public API names unambiguous**: Export a single obvious function when possible; otherwise, choose names that strongly indicate which one callers should use, and back them up with precise docs.
- **Treat telemetry/property renames as breaking**: When renaming event property keys (e.g., `taskId` → `ulid`), update all call sites and ensure every emitted event uses the same key with the same meaning.

Example (replace vague booleans):
```ts
// Before
async function load(refresh: boolean, background = false) { ... }

// After (intent-revealing)
async function load(refresh: boolean, userInitiated = false) { ... }
```

Example (prefer stateful naming over booleans):
```ts
// Before
promptSeeded?: boolean;

// After
promptSource?: 'seeded' | 'written';
```