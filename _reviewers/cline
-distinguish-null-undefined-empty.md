---
title: Distinguish null, undefined, empty
description: Treat `null`, `undefined`, and "empty" values (empty string, empty array)
  as distinct states rather than assuming they are interchangeable, and pick the comparison
  operator that matches the intended semantics instead of defaulting to loose checks
  like `??` or `!== undefined`.
repository: "cline/cline\r\n"
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 70946
---

Treat `null`, `undefined`, and "empty" values (empty string, empty array) as distinct states rather than assuming they are interchangeable, and pick the comparison operator that matches the intended semantics instead of defaulting to loose checks like `??` or `!== undefined`.

Concretely:
- When parsing untrusted/external data (API responses, JSON payloads), narrow to the exact expected type rather than trusting `!== undefined`. For example, a pagination cursor should be accepted only if `typeof cursor === "string"`; otherwise a server returning `nextCursor: null` will pass an `!== undefined` check and cause an infinite loop.
- Be careful with `??` when the "falsy but present" case matters. `images ?? retry.images` does not fall back when `images` is `[]` (protobuf's default for an omitted field), silently keeping an empty list instead of the intended fallback. Use an explicit check such as `images?.length ? images : retry.images` when empty-vs-absent is semantically different.
- Use `null` and `undefined` intentionally when they mean different things across an API boundary: `undefined`/omitted should mean "leave unchanged," while an explicit `null` should mean "reset/clear." Don't fold a clear action into a value that can't express it (e.g., sending `baseUrl: null` to reset to a manifest default vs. an empty string, which is a distinct literal value). Likewise, watch for default parameters silently swallowing an explicit `undefined`; use `null` when you need a value that survives the default.
- Don't let an unexpected `null`/`undefined` silently fall through to an unsafe code path — if a helper is documented to always return a value or throw, treat an unexpected `null`/undefined result as a bug and throw explicitly rather than continuing.
- When forwarding optional fields through an API, check each field independently with `!== undefined` so omitted fields are not overwritten with stale or merged defaults.

Add regression tests for the specific null/undefined/empty edge case being fixed (e.g., a server sending a `null` cursor, a retry with an empty `images` array) so the distinction is enforced going forward.