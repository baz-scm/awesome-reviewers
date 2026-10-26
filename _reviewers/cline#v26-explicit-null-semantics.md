---
title: Explicit Null Semantics
description: 'When handling nullable/optional inputs, always preserve the *intent*
  difference between: omitted (`undefined`), explicit `null` (often “clear”), and
  empty-but-present values (`[]`, `""`). Normalize and validate at boundaries, and
  keep TypeScript and wire/persistence encoding consistent.'
repository: cline/cline#v26
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 70893
---

When handling nullable/optional inputs, always preserve the *intent* difference between: omitted (`undefined`), explicit `null` (often “clear”), and empty-but-present values (`[]`, `""`). Normalize and validate at boundaries, and keep TypeScript and wire/persistence encoding consistent.

Apply these rules:
- **Preserve intent in merges:** `??` only treats `null/undefined` as missing; empty arrays/strings are still “present” and must not be treated as omitted.
- **Align types with runtime normalization:** if you normalize `null` → omission, the function signature and downstream expectations must include `null` (or convert before calling).
- **Keep wire/persistence encodings stable:** if `metadata: null` is the protocol for “clear”, don’t change it to a literal `null` that the persistence layer interprets as “omit/no-op”.
- **Normalize model inconsistencies at ingestion:** if models send `null` where your schema expects `string`, accept `null` at runtime but convert it to omission before performing create/insert semantics.
- **Test explicit edge cases:** add tests that cover `undefined vs null vs empty`.

Example: treat “omitted” vs “explicit empty array” differently when merging retry attachments.
```ts
// Wrong if [] is semantically meaningful (protobuf omitted => [])
const merged = images ?? retry.images;

// Prefer explicit checks for omission-like cases
const merged = images && images.length > 0 ? images : retry.images;
// or: if you can detect “field was omitted” use that signal instead of []
```

Example: keep “clear” vs “no-op” stable for persistence.
```ts
// If the persistence layer interprets null as “omit”, encode clears explicitly
const payload = updates.metadata === null
  ? { metadata: {} } // clear semantics
  : { metadata: updates.metadata };
```