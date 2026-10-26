---
title: Null semantics consistency
description: When a field can be omitted, `undefined`, `null`, or an empty value,
  treat those as *different meanings*—and make that meaning consistent across types,
  validation/schema, serialization, and downstream integrations. Don’t rely on `??`/defaulting
  to “do the right thing” implicitly.
repository: cline/cline#v9
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70868
---

When a field can be omitted, `undefined`, `null`, or an empty value, treat those as *different meanings*—and make that meaning consistent across types, validation/schema, serialization, and downstream integrations. Don’t rely on `??`/defaulting to “do the right thing” implicitly.

Practical rules:
1) **Normalize at boundaries with explicit logic**
   - Decide: does `null` mean “clear”, “unknown”, or “omitted”?
   - Convert `null/undefined` to one internal representation early (but preserve “clear” vs “no update”).
2) **Align TS types + zod schemas + runtime normalization**
   - If the runtime normalizes `null`, the type should reflect `null` (not `undefined`) or vice-versa.
   - If the schema only advertises strings, normalize `null` to omission in the code path that builds/uses the payload.
3) **Differentiate “omitted” vs “empty”**
   - Omitted fields may decode as `[]` by some transports (e.g., protobuf). In those cases, treat empty as “provided but empty” rather than “missing”.
4) **Preserve explicit clears across serialization layers**
   - If a downstream system treats `metadata: null` as “clear”, ensure your wire encoding preserves that behavior (tests for the semantic boundary are non-negotiable).
5) **Be careful with external APIs that treat missing/incorrect keys as NULL**
   - Named-parameter binding rules can turn a mistake into a silent “NULL everywhere” query.

Example pattern (different meanings for omission vs provided empty):
```ts
// Intention: use fallback only when the response truly omitted attachments,
// not when it explicitly provided an empty list.
function resolveImages(responseImages: string[] | undefined, fallback: string[]) {
  // If transport turns “omitted” into `[]`, you must detect intent differently.
  // If `responseImages` is defined but empty, treat it as provided.
  return responseImages !== undefined ? responseImages : fallback;
}

// If you must also treat some `null` as omission:
function normalizeOldText(oldText: string | null | undefined) {
  return oldText === null ? undefined : oldText;
}
```

Add tests that cover: `undefined`, `null`, empty (`[]` / `""`), and “meaningful value”, especially across serialization/validation boundaries.