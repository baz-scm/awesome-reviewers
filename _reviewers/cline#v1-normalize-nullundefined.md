---
title: Normalize null/undefined
description: At API/persistence/backend boundaries, treat `null`, `undefined`, omission,
  and empty values as *semantically different*. Normalize and encode intent explicitly—especially
  for “clear/reset” vs “leave unchanged”.
repository: cline/cline#v1
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70862
---

At API/persistence/backend boundaries, treat `null`, `undefined`, omission, and empty values as *semantically different*. Normalize and encode intent explicitly—especially for “clear/reset” vs “leave unchanged”.

Practical rules:
- **Explicit clear must use the downstream’s clear encoding.** Don’t assume `null` and `{}` are interchangeable; persistence layers may decode `null` as “omitted”.
- **Model types after the real normalization.** If runtime turns `null` into “no intent”, make the signature reflect that (`null` vs `undefined`) so the type checker guards the behavior.
- **Avoid `??` when empty is meaningful.** For fields like attachments where `[]` can mean “intentionally none” or “omitted by decoder”, decide using semantic checks (e.g., non-empty) rather than nullishness.
- **Backend integration must match exact parameter naming.** If a backend binds missing/mismatched named params to SQL `NULL`, ensure query parameters use the exact tokens it expects.
- **Boolean precedence must be deterministic.** When both legacy and new flags exist, implement the documented precedence (and handle case-insensitive boolean spellings if parsed from text).

Example patterns:
```ts
// 1) Explicit reset vs omission
// Good: explicit reset shape/value so the receiver performs a clear.
await connection.update({ baseUrl: null });

// 2) Optional array merging: don’t use `??` if `[]` can be a decoder default.
const effectiveImages = images && images.length > 0 ? images : retry.images;

// 3) Type reflects runtime normalization
function resolveReasoning(req: GatewayStreamRequest, ctx: Context) {
  // If runtime accepts `null` as an explicit "no intent", the type should too.
}
```
Applying this prevents “no-op clears”, incorrect merges where empty overwrites intended values, and subtle backend differences where missing parameters behave like `NULL`.