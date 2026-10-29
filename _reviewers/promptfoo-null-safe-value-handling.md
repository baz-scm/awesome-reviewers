---
title: Null-safe value handling
description: When a value may be null, undefined, or structurally different than expected
  (e.g. legacy/persisted data, external input, or an intentionally empty override),
  don't assume its shape or truthiness — check explicitly and fail safe.
repository: promptfoo/promptfoo
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 26565
---

When a value may be null, undefined, or structurally different than expected (e.g. legacy/persisted data, external input, or an intentionally empty override), don't assume its shape or truthiness — check explicitly and fail safe.

- Prefer `??` over `||` when a legitimate falsy value (empty string, 0, false) must be preserved rather than treated as "absent." For example, an explicit empty API-key override (`namedKey = ''`) should not fall through to an unrelated default: use `namedKey ?? fallback`, not `namedKey || fallback`.
- Before calling array-only operations (`.map`, `.length`, iteration) on a field that may come from legacy, malformed, or externally-supplied data, verify the actual shape first (`Array.isArray(...)`) and provide a safe fallback (empty array/zero) instead of crashing or silently producing wrong results. For example:
  ```ts
  if (!Array.isArray(table.body)) {
    return 0; // don't attempt table.body.length on malformed/legacy payloads
  }
  return table.body.length;
  ```
- When iterating arrays for validation, be aware that methods like `.some()`/`.every()` skip holes in sparse arrays; use `for...of` (or `Array.from`) when every index — including holes treated as `undefined` — must be checked.
- Keep type declarations/schemas in sync with actual null-handling semantics: if `null` is a supported "clear this value" signal in the implementation, the corresponding input types/schemas must accept `null` too (and vice versa — don't silently widen internal types to accept `null` just to satisfy a test; validate through the proper public API boundary instead).
- Avoid over-guarding operations that are already null/undefined-safe (e.g. spreading `undefined` into an object yields `{}`, which is often fine); only add guards where the downstream consumer actually requires one.

Applying these checks consistently prevents silent data corruption, unexpected fallback to wrong defaults, and runtime crashes (e.g. 500s) when processing data whose null/empty/shape state deviates from the happy path.</description>
