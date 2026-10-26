---
title: Normalize Null Boundaries
description: Always handle `null`/`undefined`/omitted values explicitly at the edges
  of your system (parsing, schema validation, adapter code, and external calls). Don’t
  rely on generic fallback operators or truthiness—define the semantics (“missing
  vs explicit empty”), normalize immediately, and add tests.
repository: cline/cline#v25
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70891
---

Always handle `null`/`undefined`/omitted values explicitly at the edges of your system (parsing, schema validation, adapter code, and external calls). Don’t rely on generic fallback operators or truthiness—define the semantics (“missing vs explicit empty”), normalize immediately, and add tests.

Practical rules:
- Encode precedence when multiple fields can represent the same concept (e.g., `disabled` vs legacy `enabled:false`).
- Normalize `null` from upstream models/sources into the representation you actually want (often “omit” rather than “null”).
- Distinguish omitted fields from meaningful empty values. For arrays, use semantic checks rather than `??`.
- Validate required companion inputs for optional features; fail fast (or disable actions) instead of silently falling back.
- When calling external systems, ensure parameter/token names match exactly to avoid accidental `NULL` binding.

Example patterns:
```ts
// 1) Precedence + explicit boolean parsing
export function isFrontmatterDisabled(data: Record<string, unknown>): boolean {
  if (typeof data.disabled === "boolean") return data.disabled;
  return data.enabled === false;
}

// 2) Missing vs empty array (protobuf omitted -> []), prefer original unless non-empty arrives
function pickImages(retryImages: string[], incomingImages?: string[]): string[] {
  return incomingImages?.length ? incomingImages : retryImages;
}

// 3) Schema-side normalization: advertise strings, treat model-provided null as omitted
// (conceptual)
// schema allows null, but transform null -> undefined/omitted at runtime
```

Checklist:
- Add unit/e2e tests for each boundary case: `null`, `undefined`, omitted, and explicit empty values.
- Prefer explicit conversions (`null` → omission, `[]` → “empty”) over implicit operators (`??`, `||`) unless the semantics are proven correct.