---
title: Null Semantics Contract
description: Treat `null`, `undefined`, and “omitted field” as distinct protocol states.
  Ensure the meaning is consistent across TypeScript types, runtime normalization,
  validation schemas, and any persistence/transport encoding/decoding—especially for
  reset/clear paths.
repository: cline/cline#v20
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70886
---

Treat `null`, `undefined`, and “omitted field” as distinct protocol states. Ensure the meaning is consistent across TypeScript types, runtime normalization, validation schemas, and any persistence/transport encoding/decoding—especially for reset/clear paths.

Apply this standard:
1) **Define meaning**: Decide what `null` means vs `undefined` vs omission (e.g., “reset to manifest default”, “use existing value”, “unspecified”).
2) **Enforce at the boundary**: Update TS types and schemas so signatures match runtime normalization. Don’t widen types “halfway”.
3) **Normalize before use**: Convert `null` to omission (or vice versa) in exactly one place—near the boundary—then rely on the normalized shape.
4) **Encode exactly what the downstream expects**: If the persistence layer interprets `null` as “omitted”, then a “clear” must be encoded as the form it actually understands (e.g., `{}` vs `null`).
5) **Test transitions**: Add tests for the full matrix: `undefined` vs `null` vs missing, plus “reset to default” and “clear” behavior.

Example pattern (normalize + explicit encoding):
```ts
type UpdateInput = {
  baseUrl?: string | null; // null = explicit reset; undefined = keep
};

type WireUpdate = { baseUrl?: string | null };

function normalizeBaseUrl(input: UpdateInput): WireUpdate {
  // Boundary normalization: only accept the three states.
  if (!('baseUrl' in input)) return {};              // omitted => keep
  if (input.baseUrl === null) return { baseUrl: null }; // encoded reset
  return { baseUrl: input.baseUrl };               // explicit value
}
```
Rule of thumb: if a field is used for a **reset/clear**, make its representation unambiguous and verified end-to-end with tests.