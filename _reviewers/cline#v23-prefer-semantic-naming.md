---
title: Prefer semantic naming
description: Names should encode meaning and guarantees—not just types. When an identifier
  represents a state or a usage decision, make that state/decision explicit, consistent,
  and aligned with existing conventions.
repository: cline/cline#v23
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 70889
---

Names should encode meaning and guarantees—not just types. When an identifier represents a state or a usage decision, make that state/decision explicit, consistent, and aligned with existing conventions.

Practical rules:
1) Avoid vague/negated flags
- If a parameter is really “user-initiated” vs “background”, name it that way.

2) Don’t use booleans for richer domain states
- Prefer a string/enum that directly describes the state (positive naming), e.g. `entry: 'run' | 'continue'` rather than `isPromptSeeded: boolean` when callers need to understand what “false” means.

3) Public API names must make the right choice obvious
- If multiple exported functions differ by subtle semantics, either export one canonical function or rename to strongly hint which one callers should use.

4) Follow existing naming conventions by ownership/origin
- If the codebase distinguishes caller-supplied vs system/envelope-added fields (e.g., camelCase context keys vs snake_case envelope/global fields), keep that distinction.

5) Keep identifiers aligned with shared types/constants
- When a shared type exists (e.g., `ClientName`), use it rather than inventing parallel string literals—this prevents host/client drift.

Example (flag rename):
```ts
// Before
const load = useCallback(async (refresh: boolean, background = false) => {
  if (!background) {
    // ...
  }
});

// After
const load = useCallback(async (refresh: boolean, userInitiated = false) => {
  if (userInitiated) {
    // ...
  }
});
```