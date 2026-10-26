---
title: Normalize Null Semantics
description: Null/undefined/empty values must retain meaning across boundaries (UI
  → controller, schema → protocol, protocol → persistence). Avoid implicit coercions
  that turn clears into no-ops or fallbacks into overwrites.
repository: cline/cline#v4
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70864
---

Null/undefined/empty values must retain meaning across boundaries (UI → controller, schema → protocol, protocol → persistence). Avoid implicit coercions that turn clears into no-ops or fallbacks into overwrites.

Apply these rules:
- **Define meaning up front:** Treat `undefined` as “not provided/keep existing”, `null` as “explicitly cleared/reset”, and empty arrays/strings as **intentional values** only if that’s what the contract expects.
- **Normalize at the boundary:** If models/clients send `null` for fields you want as optional, normalize immediately (e.g., convert `null` to omission) rather than letting downstream code guess.
- **Use the exact wire/reset form:** When clearing/resetting persisted fields, send the representation the persistence layer expects (e.g., distinguish `{}` vs `null`, or `baseUrl: null` vs `baseUrl: ""`).
- **Gate side effects on explicit stored state:** Only clear/overwrite identity/tokens/settings when the input indicates the replacement scenario (don’t infer from trimmed/unchanged values).
- **Make fallback depend on presence vs emptiness:** For retries/merges, don’t treat `[]` the same as “omitted”; decide based on `images?.length` (or a similar presence check).
- **Lock it in with tests:** Add regression tests for “field omitted”, “field provided as empty”, and “field provided as null/clear”.

Example pattern (fallback depends on actual provided content):
```ts
async function applyRetry(images?: string[], files?: string[], retryImages?: string[]) {
  // protobuf may decode omitted images as []
  const finalImages = images && images.length > 0 ? images : retryImages;
  // likewise for files
  return { images: finalImages, files };
}
```

This prevents subtle regressions like: resets not happening, identity being cleared on unchanged inputs, or defaulting overriding an explicit empty value.