---
title: Semantic Naming Standards
description: 'Use names that encode the real meaning, follow shared conventions, and
  stay consistent across call sites.


  Guidelines:

  1) Prefer canonical/shared identifier names'
repository: cline/cline#v30
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70894
---

Use names that encode the real meaning, follow shared conventions, and stay consistent across call sites.

Guidelines:
1) Prefer canonical/shared identifier names
- If the codebase has a standard (e.g., a `ClientName` union), use it instead of ad-hoc strings/types.

2) Avoid vague booleans; use positive, enum-like values
- If a field can mean different states, don’t force it into `true/false`. Use string-literal states that describe the situation.

3) Keep payload key casing/format consistent with established origin rules
- For telemetry/event payloads: caller-supplied `context` keys should follow the context naming style (commonly camelCase), while envelope/global enrichment keys should follow the established alternate style (commonly snake_case). Don’t mix meaning under the same key.

4) Renames must be meaning-safe
- When renaming an identifier property (e.g., `taskId` → `ulid`), update every call site and any join logic/consumers so the property key never contains multiple identifier formats.

5) IDs used for referencing UI/logic must be stable within the consumer’s scope
- If something (like highlight, Skip/Undo mapping, or selection) references an `id`, ensure that `id` construction stays stable for that scope.

Example (boolean → semantic string):
```ts
// Before
type Entry = { entry?: boolean }; // unclear: what does false mean?

// After
type Entry = { entry?: 'run' | 'continue' }; // explicit and self-documenting
```

Example (meaning-safe rename):
```ts
// If you change captureCheckpointUsage(userIdPropName) semantics,
// update both the helper signature and every call site so the property
// key always carries the same identifier format.
telemetryService.captureCheckpointUsage(/* pass the ulid everywhere */);
```