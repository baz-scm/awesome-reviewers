---
title: Explicit null semantics
description: Define and enforce a single meaning for `undefined` vs `null` vs “field
  omitted” at every boundary (schema parsing, request translation, persistence/update
  APIs).
repository: cline/cline#v24
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 70891
---

Define and enforce a single meaning for `undefined` vs `null` vs “field omitted” at every boundary (schema parsing, request translation, persistence/update APIs).

Practical rules:
- **Treat `undefined` as “omit/keep existing”** when building update/persistence payloads.
- **Treat `null` as an explicit action** (usually “clear”), but only if the downstream layer really interprets `null` that way—otherwise normalize it to the correct representation (e.g., `{}` for “clear”).
- **Normalize at the boundary**: parse/convert `null`/`undefined` into the intended internal representation immediately, rather than relying on defaults.
- **Align TS types with runtime normalization**: if runtime intentionally accepts `null`, the types/signatures must reflect it; otherwise edge cases will silently diverge.
- **Make precedence explicit** for boolean-like legacy flags (e.g., `disabled` wins over legacy `enabled`): encode the rule once in a helper and reuse it.
- **Add tests for all edge encodings** (`undefined`, `null`, omitted) to prevent semantic regressions.

Example pattern (update payload building):
```ts
type Updates = {
  metadata?: Record<string, unknown> | null;
  prompt?: string | null;
};

function toPersistencePayload(updates: Updates) {
  return {
    // undefined => omitted (keep stored value)
    ...(updates.prompt === undefined ? {} : { prompt: updates.prompt }),

    // null => clear ONLY if the persistence layer treats it as clear
    // otherwise normalize to the expected clear token
    ...(updates.metadata === undefined
      ? {}
      : { metadata: updates.metadata === null ? {} : updates.metadata }),
  };
}
```
And for schema-driven input where models may send `null`:
- Prefer a schema that advertises the intended type (e.g., `string`) and then **runtime-normalize** `null` to “omit” rather than attempting to model all null behavior in the union/signature.