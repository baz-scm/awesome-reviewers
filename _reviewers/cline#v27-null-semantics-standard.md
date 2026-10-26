---
title: Null Semantics Standard
description: When data crosses a boundary (protobuf/webview/schema/config/sql), treat
  `null`, `undefined` (omitted), and “empty” values as distinct meanings. Be explicit
  about normalization, precedence, and required-field validation—don’t rely on implicit
  fallbacks that can silently change behavior.
repository: cline/cline#v27
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70892
---

When data crosses a boundary (protobuf/webview/schema/config/sql), treat `null`, `undefined` (omitted), and “empty” values as distinct meanings. Be explicit about normalization, precedence, and required-field validation—don’t rely on implicit fallbacks that can silently change behavior.

Apply this:
1) Normalize at the boundary
- If the runtime contract expects omission, convert inbound `null` to “omit” (not to empty string unless empty has the same meaning).
- If the contract needs an explicit reset, send explicit `null` (not `""`) so the receiver can differentiate reset vs empty literal.

2) Preserve empty but meaningful values
- If a field is meaningful when empty (e.g., `[]` from “no images provided”), don’t replace it with defaults using `??` where it would override intent.

3) Encode boolean precedence rules
- Decide which flag wins and implement it directly (e.g., `disabled: true` overrides `enabled: false` only when `disabled` is absent).

4) Validate required inputs before fallback
- If a “cloud” path requires a repository, block/disable sending rather than silently falling back to local execution.

5) Guard against platform-specific “missing => NULL” behavior
- For SQL/FFI/etc., ensure you use the exact parameter/token forms required by the runtime, and add tests to prevent regressions.

Example patterns:
```ts
// 1) Null->omit normalization (schema boundary)
function normalizeOptionalString(v: string | null | undefined): string | undefined {
  return v === null ? undefined : v;
}

// 2) Preserve empty arrays (protobuf boundary)
// If `images` is omitted, protobuf may decode to `[]`.
// Only substitute from retry when the incoming list is actually empty *and* that’s intended.
const nextImages = images.length ? images : retry.images;

// 3) Boolean precedence
function isDisabled(data: Record<string, unknown>) {
  return data.disabled === true || (data.disabled === undefined && data.enabled === false);
}
```
