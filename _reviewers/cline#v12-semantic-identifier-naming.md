---
title: Semantic Identifier Naming
description: "Use names that encode intent and domain meaning.\n\n- Avoid vague boolean\
  \ flags and negation-based semantics (rename to what triggers the behavior).\n \
  \ ```ts"
repository: cline/cline#v12
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70872
---

Use names that encode intent and domain meaning.

- Avoid vague boolean flags and negation-based semantics (rename to what triggers the behavior).
  ```ts
  // before
  async function load(refresh: boolean, background = false) {
    if (!background) { ... }
  }

  // after
  async function load(refresh: boolean, userInitiated = false) {
    if (userInitiated) { ... }
  }
  ```
- If a field describes a situation with multiple meaningful states, don’t use booleans; prefer a positive string/enum-like union (e.g., `entry?: 'run' | 'continue'`, `promptSeeded?: ...` -> `promptState?: 'seeded' | 'written'`).
- When renaming identifiers that appear in data contracts/telemetry/events, update *all* call sites and keep property names consistent (positional parameters can compile but silently corrupt meaning).
  ```ts
  // If you rename captureCheckpointUsage(taskId) -> captureCheckpointUsage(ulid),
  // ensure every call passes the matching identifier type.
  ```
- Ensure exported function names are easy to pick correctly; avoid near-duplicate names that require reading the implementation or careful inference. If multiple similar operations exist, consolidate into one “obvious” API or add naming that strongly indicates which to use.
- Follow naming/casing conventions that carry meaning (e.g., telemetry keys: caller-supplied context stays camelCase; envelope/global enrichment uses snake_case) so the casing communicates origin.