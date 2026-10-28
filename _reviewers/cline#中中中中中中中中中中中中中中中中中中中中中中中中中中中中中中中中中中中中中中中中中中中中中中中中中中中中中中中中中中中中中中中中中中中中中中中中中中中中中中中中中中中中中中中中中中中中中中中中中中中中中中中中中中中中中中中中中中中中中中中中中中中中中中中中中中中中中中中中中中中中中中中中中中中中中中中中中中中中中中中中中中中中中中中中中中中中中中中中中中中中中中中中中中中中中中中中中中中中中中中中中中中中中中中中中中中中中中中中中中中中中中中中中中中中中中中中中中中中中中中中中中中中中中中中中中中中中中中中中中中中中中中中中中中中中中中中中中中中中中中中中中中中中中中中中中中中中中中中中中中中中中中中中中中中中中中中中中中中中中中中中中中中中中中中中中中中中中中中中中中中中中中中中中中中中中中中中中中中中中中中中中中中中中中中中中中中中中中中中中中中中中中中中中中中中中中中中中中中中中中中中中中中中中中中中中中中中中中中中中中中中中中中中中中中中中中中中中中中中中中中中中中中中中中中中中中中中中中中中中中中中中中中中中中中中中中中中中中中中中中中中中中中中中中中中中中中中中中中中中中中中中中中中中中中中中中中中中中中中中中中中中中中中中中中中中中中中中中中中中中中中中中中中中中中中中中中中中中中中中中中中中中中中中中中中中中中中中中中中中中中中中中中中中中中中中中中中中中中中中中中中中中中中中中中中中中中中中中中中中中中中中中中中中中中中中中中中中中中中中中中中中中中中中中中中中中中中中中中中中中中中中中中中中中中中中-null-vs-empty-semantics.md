---
title: Null vs empty semantics
description: When a value can mean "omitted/unchanged", "explicitly cleared", or "present
  but empty", treat these as distinct states end-to-end and verify that each boundary
  (serialization, merge logic, nullish coalescing, spreads) preserves the intended
  meaning instead of collapsing them together.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70986
---

When a value can mean "omitted/unchanged", "explicitly cleared", or "present but empty", treat these as distinct states end-to-end and verify that each boundary (serialization, merge logic, nullish coalescing, spreads) preserves the intended meaning instead of collapsing them together.

Concretely:
- Do not assume `undefined`/missing always signals "no data": some transports (e.g. protobuf) decode an omitted field as `[]` or `""`, not `undefined`/`null`. Using `value ?? fallback` in that case silently drops the fallback even when the caller intended "nothing was sent." Check the actual emptiness condition (e.g. `value?.length ? value : fallback`) rather than relying on `??`.
- When an API needs to express an explicit "clear this field" vs "leave it unchanged," pick a sentinel (commonly `null` for clear, `undefined`/omitted for unchanged) and make sure every layer that encodes/decodes or merges the payload honors that contract. For example, re-encoding a partial update must not turn an explicit `metadata: null` clear into an omitted field that a downstream decoder treats as "no change" — write a regression test asserting the clear still takes effect after any refactor of the encoding.
- When a fallback or recovery path depends on an invariant ("this call always returns a value or throws"), do not silently continue into a less-safe branch if that invariant is violated; throw explicitly so the null-like edge case is impossible to miss instead of falling through to code that assumes a non-null value.
- Prefer constructing nullable/optional state as fully-initialized where possible (e.g., initialize a deferred promise in the constructor rather than lazily creating it on first access) to eliminate unnecessary `?`/optional-chaining and the conditionals they require at every call site.

Example of the clear-vs-omit pitfall:
```ts
// BAD: spreading only when defined collapses "clear" (null) into "omitted"
...(updates.metadata !== undefined ? { metadata: updates.metadata } : {})
// a caller passing `metadata: null` to clear the field must still reach the
// wire as `{}`/`null` per the receiving layer's contract — verify this with a test,
// don't assume `!== undefined` is enough once you change the encoding.
```