---
title: Nullish vs falsy checks
description: Be deliberate about how falsy, null, undefined, and "unknown" values
  are distinguished and defaulted. The `??` operator only falls back for `null`/`undefined`,
  so it will happily pass through other falsy-but-valid-looking values like `0`, which
  can break logic that assumes a positive number (e.g. a `0` timeout silently causing
  every request to abort...
repository: decolua/9router#zz237855c
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 31752
---

Be deliberate about how falsy, null, undefined, and "unknown" values are distinguished and defaulted. The `??` operator only falls back for `null`/`undefined`, so it will happily pass through other falsy-but-valid-looking values like `0`, which can break logic that assumes a positive number (e.g. a `0` timeout silently causing every request to abort immediately). When a value of `0` (or empty string, `NaN`, etc.) should also trigger the default, use `||` instead of `??`, or explicitly sanitize the value before combining fallbacks:

```js
// Bad: `0` is a valid value for `??`, so a configured timeoutMs of 0 is kept as-is
const timeoutMs = sanitizedOverride ?? this.config?.timeoutMs ?? FETCH_CONNECT_TIMEOUT_MS;

// Good: fall back when the value is falsy (covers 0, undefined, null, etc.)
const timeoutMs = sanitizedOverride ?? (this.config?.timeoutMs || FETCH_CONNECT_TIMEOUT_MS);
```

Similarly, when a value's "truthiness" is used directly in a boolean condition, coerce it explicitly with `!!` so object/number/string values don't produce unintended results:

```js
// Bad: reasoning_effort could be 0, an empty string, or an object — ambiguous
const hasThinkingMode = result.reasoning_effort || result.thinking?.type === "enabled";

// Good: explicit coercion makes intent clear
const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
```

Finally, apply the same "unknown" semantics consistently across related code paths. If one part of the system treats a missing/unknown value as disqualifying for an aggregate computation (e.g. dropping `contextWindow` entirely when any seat's context length is unknown), parallel logic elsewhere (e.g. combo capability aggregation) must use the identical rule rather than silently computing over only the known values:

```js
const contexts = allCaps.map((c) => c.contextWindow);
const ctxKnown = contexts.every(Number.isFinite);
...(ctxKnown ? { contextWindow: Math.min(...contexts) } : {}),
```

When writing null/undefined/falsy-handling logic, document which values are intentionally treated as "missing" and add a regression test covering the zero/unknown edge case.</description>
