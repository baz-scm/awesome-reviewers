---
title: Explicit API Contracts
description: When designing or evolving exported/public APIs (tools, bindings, and
  types), make the interface shape and behavioral contract explicit and schema-friendly.
repository: facebook/react#b2
label: API
language: JavaScript
comments_count: 3
repository_stars: 251882
---

When designing or evolving exported/public APIs (tools, bindings, and types), make the interface shape and behavioral contract explicit and schema-friendly.

- Prefer an options bag over positional optional parameters for extensible inputs.
  - This aligns with schema-based tooling (e.g., expecting an object of arguments) and avoids breaking changes when new flags are added.
- Define and enforce consistent required/optional semantics across bindings/consumers.
  - If one consumer supplies `integrity`/`fetchPriority`, ensure all bindings follow the same contract (or clearly encode which values are required vs defaulted).
- Encode substitutability in types via variance annotations when it affects how values can be used.

Example (options bag):
```ts
// Prefer
getComponentByUid(uid: string, opts?: {includeHooks?: boolean})

// Over
getComponentByUid(uid: string, includeHooks?: boolean)
```

Practical checks before merge:
- Can future parameters be added without changing positional call sites? If not, switch to an options bag.
- Do all bindings that call into the same API supply/omit the same fields under the same rules? If not, make the contract explicit (and align behavior).
- Do type definitions reflect intended variance (so callers get correct assignability errors/success)? Adjust variance annotations accordingly.