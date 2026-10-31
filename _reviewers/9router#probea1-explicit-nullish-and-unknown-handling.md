---
title: Explicit nullish and unknown handling
description: Be deliberate about what counts as "missing" versus a valid-but-falsy
  value, and keep unknown/null propagation consistent across all code paths that derive
  from the same data.
repository: decolua/9router#probeA1
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 31730
---

Be deliberate about what counts as "missing" versus a valid-but-falsy value, and keep unknown/null propagation consistent across all code paths that derive from the same data.

- Choose `??` only when 0, false, or "" are legitimate values that should NOT trigger a fallback; otherwise use `||` (or an explicit `Number.isFinite`/truthy check) so that values like `timeoutMs: 0` don't silently become invalid inputs.
  ```js
  // Wrong: 0 is a valid-looking config value but breaks setTimeout semantics
  const timeoutMs = sanitizedOverride ?? this.config?.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  // Right: explicitly treat 0/falsy config as "unset"
  const timeoutMs = sanitizedOverride ?? (this.config?.timeoutMs || DEFAULT_TIMEOUT_MS);
  ```
- When combining nullable/optional fields in boolean logic, coerce explicitly with `!!` rather than relying on mixed-type truthiness, so the resulting flag is an unambiguous boolean:
  ```js
  const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
  ```
- When a value can be "unknown" (missing/undefined) and is aggregated or derived in multiple places (e.g., combo capability limits computed both in an aggregation function and in a route handler), apply the same unknown-propagation rule everywhere. If any contributing member is unknown, the derived value must also be unknown/dropped — never silently compute from only the known subset, as that can produce a value that contradicts an "unknown" flag set elsewhere:
  ```js
  const contexts = allCaps.map((c) => c.contextWindow);
  const allKnown = contexts.every(Number.isFinite);
  const aggregated = { ...(allKnown ? { contextWindow: Math.min(...contexts) } : {}) };
  ```
  Add a test covering a mixed known/unknown combo to ensure nested and top-level unknown flags stay in sync.</description>
