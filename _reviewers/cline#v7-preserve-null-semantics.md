---
title: Preserve null semantics
description: When a system distinguishes “absent”, “explicitly cleared (null)”, and
  “empty value” ("", []), you must preserve those states end-to-end—types, serialization,
  SQL/FFI bindings, and control flow.
repository: cline/cline#v7
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70865
---

When a system distinguishes “absent”, “explicitly cleared (null)”, and “empty value” ("", []), you must preserve those states end-to-end—types, serialization, SQL/FFI bindings, and control flow.

Practical rules:
- Model states explicitly: if `null` has meaning (clear/reset), encode it as `null` (not `{}`, not `undefined`) and reflect that in the function signature. Don’t rely on defaults that swallow `undefined` when `null` must be treated differently.
- Don’t use `??` when empty values are meaningful.
  - For arrays where omitted vs empty differs (e.g., retry attachments), prefer presence/length checks:

```ts
// Wrong if [] means “no attachments provided” vs omitted meaning “use fallback”
const next = images ?? retry.images;

// Prefer explicit intent checks
const next = images?.length ? images : retry.images;
```
- Keep serialization/DB token semantics exact.
  - SQL named parameters must use the exact token form required by the runtime; otherwise some engines bind NULL and your WHERE logic silently fails.
- Add regression tests for semantic clears and runtime-specific behavior (e.g., “clear metadata resets persisted state” and “Bun sqlite binds prefixed named params correctly”).

If you’re unsure whether the contract distinguishes `null` vs `undefined` vs empty, treat them as different states until proven otherwise, and add a targeted test capturing the expected outcome.