---
title: Model Limits Correctness
description: When integrating LLM providers, treat model capabilities and token limits
  as *schema-variant inputs* and enforce conservative, well-tested limit computation.
repository: CLINE/cline
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70839
---

When integrating LLM providers, treat model capabilities and token limits as *schema-variant inputs* and enforce conservative, well-tested limit computation.

Apply:
1) Parse provider model-list metadata defensively
- Recognize multiple field names for the same concept (e.g., context/window).
- If a key is missing, prefer provider-specific supported fields over generic fallbacks.

Example:
```ts
function contextWindowFromCatalog(entry: Record<string, unknown>) {
  // vLLM commonly uses `max_model_len`.
  const candidates = [
    entry.context_length,
    entry.max_model_len,
    entry.contextWindow,
  ];
  for (const c of candidates) {
    if (typeof c === "number" && Number.isFinite(c) && c > 0) return Math.trunc(c);
  }
  return undefined;
}
```

2) Select defaults per provider, not globally
- Use provider manifest defaults when present (and skip placeholder/local “default” entries).
- Only then apply a global fallback.

3) Compute max-output caps with an intentional policy
- Use floors as floors (don’t apply proportional logic in a way that lowers existing allowances).
- Keep existing model/context clamps as the final safety net.

Rule of thumb:
- If a fraction of model output budget is used, ensure it only *raises* above the baseline floor; avoid accidental reductions that increase truncation/retry rates.

4) Recovery retries must separate “attempted” vs “judged”
- Retry logic may compact and retry, but it must not duplicate the run loop’s accept/reject verdict.
- Telemetry should describe the action performed and observed finish reason, not claim the outcome.

5) Pin correctness with tests; avoid downstream vendor special-casing
- If correctness depends on adapter/resolver behavior (e.g., whether reasoning fields are accepted), cover it with targeted tests.
- If you’re forced into vendor-specific handling, strongly consider fixing the upstream adapter/resolver so downstream code stays generic.

This standard prevents silent regressions like wrong context-window defaults, accidental output-cap reductions that trigger more truncation, and malformed vendor requests caused by ad-hoc special handling.