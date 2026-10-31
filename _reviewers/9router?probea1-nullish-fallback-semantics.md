---
title: Nullish fallback semantics
description: When writing fallback chains or boolean checks involving optional/nullable
  values, be explicit about whether falsy-but-valid values (0, "", false) should be
  treated as "missing" or as legitimate data, and apply that decision consistently
  everywhere the same value is consumed.
repository: decolua/9router?probeA1
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 31730
---

When writing fallback chains or boolean checks involving optional/nullable values, be explicit about whether falsy-but-valid values (0, "", false) should be treated as "missing" or as legitimate data, and apply that decision consistently everywhere the same value is consumed.

- Prefer `??` only when 0/""/false are valid, meaningful values that should NOT trigger a fallback. Prefer `||` when any falsy value (including 0) should be treated as "not configured" and fall through to a default. Mixing these inconsistently causes subtle bugs, e.g. switching `this.config?.timeoutMs || DEFAULT` to `??` silently allows `timeoutMs: 0` to disable the timeout immediately instead of using the default:
```js
// Wrong: timeoutMs: 0 bypasses the intended default and aborts immediately
const timeoutMs = sanitizedOverride ?? this.config?.timeoutMs ?? FETCH_CONNECT_TIMEOUT_MS;

// Right: 0 is treated as "unset" for this field, consistent with prior behavior
const timeoutMs = sanitizedOverride ?? (this.config?.timeoutMs || FETCH_CONNECT_TIMEOUT_MS);
```

- When a value may be "unknown" (missing/non-finite) and is aggregated or derived in multiple places, use the same unknown-propagation rule everywhere. Don't let one code path silently drop the unknown while another path aggregates over only the known values, since that produces inconsistent/contradictory output for the same logical field:
```js
const contexts = allCaps.map((c) => c.contextWindow);
const ctxKnown = contexts.every(Number.isFinite);
...(ctxKnown ? { contextWindow: Math.min(...contexts) } : {}), // drop if any unknown, matching other consumers
```

- When using a non-boolean value (e.g. a number or string) directly in a boolean condition, explicitly coerce it with `!!` so the intent is clear and edge cases (0, "", null) are handled predictably:
```js
const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
```

Add a focused test for any shared "unknown"/"missing" value to ensure all consumers agree on its treatment, and review diffs that change `||` to `??` (or vice versa) with extra scrutiny for valid falsy inputs.</description>
</invoke>
