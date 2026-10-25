---
title: Normalize Null And Undefined
description: Treat nullability as a semantic distinction, not just a type system detail.
  Normalize and apply explicit precedence at boundaries, preserve the difference between
  “omitted” and “present-but-empty”, and make TypeScript reflect runtime normalization.
repository: CLINE/CLINE
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70837
---

Treat nullability as a semantic distinction, not just a type system detail. Normalize and apply explicit precedence at boundaries, preserve the difference between “omitted” and “present-but-empty”, and make TypeScript reflect runtime normalization.

Practical rules:
1) Enforce precedence in one helper (don’t spread checks around). Example:
```ts
export function isFrontmatterDisabled(data: Record<string, unknown>): boolean {
  // `disabled:true` wins; legacy `enabled:false` only applies when disabled is absent.
  if (typeof data.disabled === "boolean") return data.disabled
  return data.enabled === false
}
```
2) Distinguish omitted vs empty after decoding. If protobuf/schema decoding turns an omitted field into `[]`, fall back based on emptiness, not only nullish coalescing:
```ts
// If `images` is [] but the caller intended “no attachments provided”, keep the retry’s originals.
const nextImages = images?.length ? images : retry.images
```
3) Align types with runtime normalization: if runtime converts `null` → “handled/omitted”, ensure the function signature and downstream expectations model `null` (not `undefined`). Prefer a small normalizer at entry.
4) Avoid Optional-state conditionals where possible: encode “set vs unset” in a type/shape (or initialize in the constructor) so callers don’t rely on `?`/null checks.
5) Compute derived booleans from raw values before formatting/transforming. If content presence affects control flow, base it on the unformatted raw input (e.g., trimmed text and provided arrays), then format.

Add tests that cover the semantic edges: both conflicting flags, boolean casing variants, omitted vs empty arrays, and null vs undefined behavior.