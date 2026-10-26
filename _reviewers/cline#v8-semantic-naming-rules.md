---
title: Semantic Naming Rules
description: 'Identifiers should be unambiguous about domain meaning, follow existing
  naming/casing conventions, and remain semantically consistent across renames.

  '
repository: cline/cline#v8
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70867
---

Identifiers should be unambiguous about domain meaning, follow existing naming/casing conventions, and remain semantically consistent across renames.

Apply these rules:
1) Prefer semantic, positive names over vague flags
- Rename unclear booleans/params to what they *mean* (not how they’re used).
- If the value is not truly a boolean, model it as an enum-like string.

Example:
```ts
// Before
async function load(refresh: boolean, background = false) { /* ... */ }

// After
async function load(refresh: boolean, userInitiated = false) { /* ... */ }
```

```ts
// Before
entry?: boolean; // “true” means what?

// After
entry?: "run" | "continue";
```

2) Avoid jargon or undefined terms
- If you must use internal metaphors (e.g., “pointer”, “dangling”), add a clear file/function-level explanation or rename so the intended concept matches what readers will assume.

3) Make exported APIs easy to choose
- If multiple exported helpers exist, their names must clearly indicate when to call which.
- When possible, export one obvious “do the right thing” function; keep others private or clearly marked for special cases.

4) Enforce casing by origin (don’t guess)
- Use camelCase for caller-supplied `context` keys.
- Use snake_case for telemetry/envelope enrichment keys.

5) Renames must update call sites and preserve semantic meaning
- Renaming parameters/properties that encode identifiers (e.g., `taskId` → `ulid`) must include updating all positional call sites so event payloads remain consistent and joinable.

If a name forces readers to open the implementation to understand intent, or if renaming can silently change semantics without type errors, that’s a naming-convention violation.