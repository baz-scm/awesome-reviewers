---
title: Explicit nullish and truthiness handling
description: 'When choosing a fallback or default for a potentially missing value,
  be deliberate about whether `0`, `''''`, or other falsy-but-defined values should
  be treated as valid or as "missing". `??` only falls back on `null`/`undefined`,
  so `config.timeoutMs ?? DEFAULT` will happily pass through a `timeoutMs: 0`, which
  may be semantically invalid (e.g. it causes...'
repository: decolua/9router#probeB7
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 31737
---

When choosing a fallback or default for a potentially missing value, be deliberate about whether `0`, `''`, or other falsy-but-defined values should be treated as valid or as "missing". `??` only falls back on `null`/`undefined`, so `config.timeoutMs ?? DEFAULT` will happily pass through a `timeoutMs: 0`, which may be semantically invalid (e.g. it causes requests to abort immediately). If zero/empty values are also invalid for your use case, use `||` (or an explicit check) instead of `??`:

```js
// Bad: 0 is treated as a valid timeout and breaks downstream logic
const timeoutMs = override ?? (this.config?.timeoutMs ?? DEFAULT);

// Good: explicitly reject invalid falsy values where appropriate
const timeoutMs = override ?? (this.config?.timeoutMs || DEFAULT);
```

Similarly, when deriving booleans from values that may be `undefined`, `0`, or other non-boolean truthy/falsy types, coerce explicitly with `!!` to avoid leaking the raw value or producing inconsistent types in combined conditions:

```js
// Bad: result may be a number/undefined instead of a boolean
const hasThinkingMode = result.reasoning_effort || result.thinking?.type === "enabled";

// Good: explicit boolean coercion
const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
```

When a value may be "unknown" (missing/undefined) and is aggregated or combined with other known values (e.g. computing a min/max across multiple sources), define one consistent rule for how "unknown" propagates and apply it everywhere that aggregation happens. For example, if one function drops a field entirely when any input is unknown, don't have a sibling function silently ignore the unknown value and compute over the known subset only — this produces different, inconsistent results for the same data and can misrepresent capabilities to consumers. Add a test that exercises mixed known/unknown inputs to catch any future drift between the two implementations.