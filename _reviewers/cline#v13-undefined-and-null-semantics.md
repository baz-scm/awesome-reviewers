---
title: Undefined and Null Semantics
description: Establish explicit, type-aligned semantics for how each optional field
  is treated when it is `undefined`, `null`, omitted, or an empty value—and enforce
  them with signatures plus targeted tests. Most null-handling bugs here come from
  subtle differences (e.g., protobuf omits → decodes as `[]`, or default parameters
  swallow an explicit `undefined`).
repository: cline/cline#v13
label: Null Handling
language: TypeScript
comments_count: 8
repository_stars: 70874
---

Establish explicit, type-aligned semantics for how each optional field is treated when it is `undefined`, `null`, omitted, or an empty value—and enforce them with signatures plus targeted tests. Most null-handling bugs here come from subtle differences (e.g., protobuf omits → decodes as `[]`, or default parameters swallow an explicit `undefined`).

Apply this standard:
- Define an “interpretation rule” per field: what should happen when the input is `undefined` vs `null` vs `[]` (or empty string).
- Make function signatures reflect runtime normalization (e.g., if code normalizes `null`, the signature must accept `null`, not `undefined`).
- When optional inputs participate in merges/retries, don’t use `??` blindly: treat empty arrays intentionally.
- Where a value is effectively always present after construction, initialize once and keep it non-null to avoid conditional `?.`/allocation.
- Ensure event projection/conversion pipelines propagate optional fields consistently.
- Add tests for the real wire/serialization behavior (omitted fields, explicit `undefined`, explicit `null`).

Example pattern (retry-style “empty array vs missing”):
```ts
async function retryWithAttachments(params: {
  images?: string[];          // from UI/proto (may decode to [])
  retryImages: string[];
}) {
  const { images, retryImages } = params;
  // Rule: only use caller images if they’re actually present and non-empty.
  const finalImages = images?.length ? images : retryImages;
  return initTask(/*...,*/ finalImages);
}
```

If you adopt this rule consistently, you’ll prevent silent semantic drift where `undefined`/`null`/empty values change behavior unintentionally, and you’ll make TS help enforce the intended logic.