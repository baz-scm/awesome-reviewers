---
title: Explicit null/falsy semantics
description: When choosing between `??` and `||`, be explicit about whether a falsy-but-defined
  value (0, '', false) should be treated as valid or as "missing". `??` only falls
  back on `null`/`undefined`, so a config value of `0` will pass through even when
  it's semantically invalid (e.g. a 0ms timeout), causing requests to fail immediately.
  Use `||` (or an explicit...
repository: decolua/9router#y
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 31751
---

When choosing between `??` and `||`, be explicit about whether a falsy-but-defined value (0, '', false) should be treated as valid or as "missing". `??` only falls back on `null`/`undefined`, so a config value of `0` will pass through even when it's semantically invalid (e.g. a 0ms timeout), causing requests to fail immediately. Use `||` (or an explicit sanitizer) when zero/empty must trigger the default, and reserve `??` for cases where 0/false are legitimate values:

```js
// 0 is not a valid timeout, so fall back on it explicitly
const timeoutMs = sanitizedOverride ?? (this.config?.timeoutMs || FETCH_CONNECT_TIMEOUT_MS);
```

Similarly, don't rely on implicit truthiness of non-boolean fields in conditionals built from mixed sources—coerce explicitly with `!!` so the check reflects intent rather than the field's underlying type:

```js
const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
```

Finally, when a value may be "unknown" (missing/null) and is aggregated or combined across multiple sources (e.g. computing a combined capability like `contextWindow`), pick one consistent rule for how unknown values propagate (e.g. "any unknown drops the whole field" vs "ignore unknowns and compute over known values") and apply it uniformly everywhere that data is derived or consumed, so that no caller can accidentally over-promise or under-report based on inconsistent null/undefined handling.