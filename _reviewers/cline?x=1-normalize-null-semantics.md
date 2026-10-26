---
title: Normalize Null Semantics
description: Treat `null`, `undefined`, and “omitted” as distinct behaviors across
  boundaries (protobuf/DTOs, schemas, persistence layers, DB bindings). Normalize
  explicitly at the edge where data enters your domain, encode the correct reset/keep
  semantics, and align TypeScript types with that normalization.
repository: cline/cline?x=1
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70861
---

Treat `null`, `undefined`, and “omitted” as distinct behaviors across boundaries (protobuf/DTOs, schemas, persistence layers, DB bindings). Normalize explicitly at the edge where data enters your domain, encode the correct reset/keep semantics, and align TypeScript types with that normalization.

Guidelines:
- For each nullable field, decide meaning for: `null` (explicit clear), `undefined` (unknown/not provided), omission (keep existing), and special empty values (`""`, `[]`)—then implement that matrix consistently.
- When downstream contracts distinguish reset vs omit, send the correct literal (e.g., a clear must be an explicit reset value rather than an empty string/object that decodes as “omitted”).
- If external systems send `null` for “not used”, normalize `null` to omission for create/insert paths (so you don’t accidentally overwrite real data).
- Ensure TS signatures match runtime normalization (`null` vs `undefined` defaults can change control flow).
- Add tests that cover “clear”, “omitted”, and “empty-but-explicit” cases for the affected fields.

Example pattern:
```ts
// Normalize external inputs to internal “omitted vs clear” semantics.
function normalizeOptionalField<T>(v: T | null | undefined): T | undefined {
  if (v === null) return undefined; // treat null-as-unset as omission
  return v; // undefined stays omitted; keep real values (including empty strings/arrays if they matter)
}

function applyRetryImages(invImages: string[] | undefined, retryImages: string[]): string[] {
  // Distinguish “explicit empty list” from “omitted by protobuf”.
  // If the request included images but it’s empty, keep it; if omitted, reuse retryImages.
  return invImages?.length ? invImages : retryImages;
}
```

Use this standard to prevent subtle regressions where clearing/renaming/superseding logic silently fails due to `null`/`undefined` mismatch or DB/serialization differences.