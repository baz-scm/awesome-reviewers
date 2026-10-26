---
title: Null intent clarity
description: Define and preserve the *meaning* of `null` vs `undefined` (and vs “empty
  but provided”) at every boundary (state, API/contracts, UI). Don’t rely on generic
  defaulting (`??`) when different “missing vs reset vs empty” behaviors matter.
repository: cline/cline#v6
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70864
---

Define and preserve the *meaning* of `null` vs `undefined` (and vs “empty but provided”) at every boundary (state, API/contracts, UI). Don’t rely on generic defaulting (`??`) when different “missing vs reset vs empty” behaviors matter.

**Standard**
1. **Codify intent in types/shape**: if `null` means “reset/unknown”, type it as `T | null` and ensure runtime normalization matches the annotation.
2. **Use precise defaulting**:
   - `undefined` (omitted) should fall back to a previous value.
   - `[]` (explicit empty) should *not* be treated as omitted.
3. **Respect precedence rules explicitly** (tri-state booleans): when two legacy flags exist, document which wins and under what absence condition.
4. **After nullifying state, update dependents**: if derived UI (toasts/locale/labels) depends on a null reset, call the update/refresh path so nothing stays stale.
5. **Add tests for the three key cases** for each field: omitted (`undefined`), explicit empty, and explicit reset (`null` or `false`).

**Example (attachments retry)**
```ts
// If protobuf omits `images`, you may get `undefined`; if it encodes empty,
// you may get `[]`—treat them differently.
const finalImages = images === undefined ? retry.images : images;
await initTask(retry.prompt, finalImages, files, undefined, undefined, retry.cloudTarget);
```

**Example (reset via null vs empty string)**
```ts
// Distinguish “reset to manifest default” from “set empty string literal”.
const update = {
  baseUrl: customBaseUrl === undefined ? undefined : customBaseUrl ?? null,
};
// Ensure the receiving contract interprets `null` as reset.
```