---
title: Null Boundary Contracts
description: 'Treat `null`/`undefined`/empty as part of the API contract: validate
  or normalize at boundaries, and never rely on fallthrough or generic `??` when “empty”
  carries meaning.'
repository: cline/cline#v23
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70889
---

Treat `null`/`undefined`/empty as part of the API contract: validate or normalize at boundaries, and never rely on fallthrough or generic `??` when “empty” carries meaning.

Apply these rules:
- **Fail fast on invariants**: if a value is required to prevent state corruption, throw when it’s missing even after a “best-effort” step—don’t fall through into alternative flows.
- **Make reset semantics explicit**: when clearing a field, send an explicit `null` (if the contract uses `null` for reset). Don’t conflate `null`, `""`, and omission.
- **Align types/schemas with real payloads**: if models emit `null` for fields you conceptually treat as optional strings, allow it in parsing but normalize at runtime (e.g., `null` → “field omitted”). Ensure TypeScript signatures match the actual normalization (`undefined` vs `null`).
- **Merge optional fields intent-aware**: when combining request/response data, don’t use `images ?? other.images` if the response may decode an omitted field as `[]`. Prefer predicates like “use other only when the new value is actually usable/non-empty”.

Example patterns:
```ts
// 1) Fail fast on invariant violation
await ensureSessionPersisted(liveSession);
if (!liveSession.artifacts) {
  throw new Error("Expected artifacts after ensureSessionPersisted");
}

// 2) Explicit null reset through the contract
await connection.update({ baseUrl: null }); // reset, do not treat as ""

// 3) Schema allows null; runtime normalizes to omission
function normalizeReplacementOldText(v: string | null | undefined) {
  return v == null ? undefined : v; // null/undefined => omit
}

// 4) Intent-preserving merge (avoid {} vs [] confusion)
function mergeImages(responseImages: string[] | undefined, fallback: string[]) {
  return responseImages && responseImages.length > 0 ? responseImages : fallback;
}
```

Result: fewer state-orphaning fallthroughs, fewer “empty means same as absent” bugs, and less drift between runtime payloads and TypeScript/schema nullability.