---
title: Null intent preservation
description: When handling nullable inputs, preserve *intent* by explicitly distinguishing
  “omitted/undefined” from “cleared/null”, and normalize at boundaries so internal
  logic doesn’t depend on incidental JS/TS defaults.
repository: cline/cline#v29
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70893
---

When handling nullable inputs, preserve *intent* by explicitly distinguishing “omitted/undefined” from “cleared/null”, and normalize at boundaries so internal logic doesn’t depend on incidental JS/TS defaults.

Practical rules:
1) Preserve wire/contract semantics
- If “clear/reset” must happen, serialize an explicit reset value (e.g., send `baseUrl: null`) rather than letting it collapse to omission.
- If “no change” is intended, omit the field (or keep it undefined) so downstream persistence doesn’t interpret it as a clear.

2) Normalize `null` at boundaries
- Treat `null` from external models/protocols as a signal: either convert it to omission for operations where `null` means “unused”, or keep an explicit reset where `null` means “clear”.

3) Avoid control-flow changes caused by missing nullable fields
- When refactoring logic that previously used a non-null catalog value, re-check how nullable/mismatched auth fields change which branch runs.

4) Lock behavior with transition tests
- Add tests for “custom → default”, “clear → persisted cleared”, and “omitted → unchanged”.

Example pattern (boundary normalization):
```ts
type Incoming = {
  // models may send null
  baseUrl?: string | null;
};

function normalizeForContract(input: Incoming): { baseUrl?: string | null } {
  // Intent: null means explicit reset; undefined means no change.
  if (input.baseUrl === null) return { baseUrl: null };
  if (input.baseUrl === undefined) return {}; // omit
  return { baseUrl: input.baseUrl }; // set
}
```

And for replacement/edit payloads:
```ts
function normalizeReplacementField(v: string | null | undefined): string | undefined {
  // For create/insert, null means “not provided”
  if (v === null) return undefined;
  return v;
}
```

This prevents the classic failure mode where a “clear” is accidentally encoded as omission and becomes a no-op.