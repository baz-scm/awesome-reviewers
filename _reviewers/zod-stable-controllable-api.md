---
title: Stable, Controllable API
description: 'When changing or adding public API in schema/validation libraries, prioritize
  a stable, user-controlled surface:


  - Avoid “deprecated-from-day-1” APIs. If an equivalent non-deprecated API already
  exists, prefer removing/migrating rather than adding new deprecated entry points.'
repository: colinhacks/zod
label: API
language: TypeScript
comments_count: 9
repository_stars: 42628
---

When changing or adding public API in schema/validation libraries, prioritize a stable, user-controlled surface:

- Avoid “deprecated-from-day-1” APIs. If an equivalent non-deprecated API already exists, prefer removing/migrating rather than adding new deprecated entry points.
- Make behavioral toggles user-configurable via `options` (e.g., allow selectively disabling specific validation checks) instead of bundling all behaviors unconditionally.
- Preserve backward compatibility in type-level changes: when introducing new generic/type parameters (e.g., adding an options-driven strictness flag), provide non-breaking defaults.
- Keep user-facing helper typing tied to the schema contract (e.g., `exemplify()` should constrain the example to the schema’s output type so changes break at compile time).
- Ensure format/shorthand APIs are “feature-complete” for the migration story (missing refinement methods becomes a blocker when deprecated methods are removed).
- Export public types that users need to compose APIs (e.g., discriminated-union option types), matching how other package types are exposed.

Example (options-based control idea):
```ts
// Don’t hard-code all hostname checks; allow opt-out per consumer need.
const schema = z.string().hostname({
  allowIPv4: true,
  allowIPv6: false,
  allowPunycode: true,
});
```