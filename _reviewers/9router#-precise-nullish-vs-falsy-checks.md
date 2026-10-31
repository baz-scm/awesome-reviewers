---
title: Precise nullish vs falsy checks
description: When writing fallback logic or presence checks, be explicit about whether
  you mean "null/undefined" or "any falsy value," and keep that semantic consistent
  across related code paths. The `??` operator only catches `null`/`undefined`, so
  swapping it in for `||` silently changes behavior when a valid value like `0` or
  `""` is allowed through. For example,...
repository: decolua/9router#
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 31729
---

When writing fallback logic or presence checks, be explicit about whether you mean "null/undefined" or "any falsy value," and keep that semantic consistent across related code paths. The `??` operator only catches `null`/`undefined`, so swapping it in for `||` silently changes behavior when a valid value like `0` or `""` is allowed through. For example, replacing `this.config?.timeoutMs || FETCH_CONNECT_TIMEOUT_MS` with `this.config?.timeoutMs ?? FETCH_CONNECT_TIMEOUT_MS` lets `timeoutMs: 0` pass through unchanged, causing every request to abort immediately instead of falling back to the default:
```js
// Wrong: 0 is treated as a valid timeout and breaks the request
const timeoutMs = sanitizedOverride ?? this.config?.timeoutMs ?? FETCH_CONNECT_TIMEOUT_MS;

// Right: explicitly fall back when timeoutMs is falsy (0 included)
const timeoutMs = sanitizedOverride ?? (this.config?.timeoutMs || FETCH_CONNECT_TIMEOUT_MS);
```
Similarly, when a field may hold a non-boolean value (e.g. a number like `reasoning_effort`), coerce it explicitly with `!!` before using it in a boolean context so `0` isn't mistaken for "unset" vs "disabled":
```js
const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
```
This same rigor applies to "unknown"/missing-value propagation across a codebase: if one code path drops a field entirely when any input is unknown, a related aggregation path must apply the same rule instead of computing a value only over the known subset, which can produce inconsistent or over-promising results downstream. Audit each fallback or coalescing expression for the exact set of values it should treat as "missing," and apply that rule uniformly everywhere the same data flows.</description>
