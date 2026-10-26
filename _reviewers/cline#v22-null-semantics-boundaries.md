---
title: Null semantics boundaries
description: Null/undefined handling must be decided per boundary (API transport,
  persistence, schema adapters, and merge logic). Treat `null`, `undefined`, omission,
  empty string, and empty array as distinct values unless the downstream contract
  explicitly says otherwise.
repository: cline/cline#v22
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70886
---

Null/undefined handling must be decided per boundary (API transport, persistence, schema adapters, and merge logic). Treat `null`, `undefined`, omission, empty string, and empty array as distinct values unless the downstream contract explicitly says otherwise.

Apply these rules:
- **Follow the contract for resets vs omission**: If a “reset” requires an explicit null, send `field: null` (don’t convert to `{}`, don’t omit). If a “no change” requires omission, omit the field entirely.
- **Align TS types with runtime normalization**: If runtime converts `null` to “omit”, the function signature should reflect that intent (avoid `| undefined` when the code normalizes `null`).
- **Preserve empties vs defaults in merges**: If a decoder turns an omitted field into an empty array (e.g., protobuf), merge logic must distinguish “user provided empty” from “user provided nothing.”
- **Document/encode precedence rules** (e.g., `disabled` beats legacy `enabled: false`) and test them.

Example pattern (choose one of the two based on contract meaning):
```ts
type Payload = { baseUrl?: string | null };

function buildBaseUrlUpdate(intent: "reset" | "set" | "noChange", value?: string): Payload {
  if (intent === "reset") return { baseUrl: null }; // explicit reset
  if (intent === "set") return { baseUrl: value ?? "" }; // explicit literal
  return {}; // no-change via omission
}
```
Also add tests for: `null` vs omitted, `""` vs `null`, and empty array vs missing array in retry/merge paths.