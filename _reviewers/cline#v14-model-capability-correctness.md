---
title: Model capability correctness
description: When integrating provider/model catalogs and gateways, treat model limits
  and feature flags (context length, reasoning support, etc.) as capability data that
  must be selected from the *correct* provider/adapter fields—never rely on generic
  fallbacks or emit features the gateway/adapters say the model doesn’t support.
repository: cline/cline#v14
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70876
---

When integrating provider/model catalogs and gateways, treat model limits and feature flags (context length, reasoning support, etc.) as capability data that must be selected from the *correct* provider/adapter fields—never rely on generic fallbacks or emit features the gateway/adapters say the model doesn’t support.

Apply these rules:
1) Prefer “actual served” limits over “advertised ceilings” when both exist (e.g., use `loaded_context_length` if present; otherwise use the ceiling field).
2) Support alternate field names across providers to avoid wrong fallbacks (e.g., vLLM’s `max_model_len`).
3) Make token-cap math semantics explicit (is a default a floor or a ceiling?), and keep existing clamps as the final safety boundary.
4) Only include reasoning-related fields if the adapter/resolver can classify support; otherwise omit them to avoid gateway rejection.
5) Avoid local one-off special casing for upstream-covered issues—prefer fixing the adapter upstream, then consume the corrected behavior.

Example (field-selection precedence):
```ts
type ModelCaps = {
  context_length?: unknown;
  context_window?: unknown;
  max_context_length?: unknown;
  loaded_context_length?: unknown;
  max_model_len?: unknown;
};

function firstPositiveInt(...values: unknown[]): number | undefined {
  for (const v of values) {
    if (typeof v === "number" && Number.isFinite(v) && v > 0) return Math.trunc(v);
  }
}

export function resolveContextWindow(c: ModelCaps): number | undefined {
  // Prefer actual served length when available; fall back to provider ceilings.
  return firstPositiveInt(
    c.loaded_context_length,
    c.context_window,
    c.max_context_length,
    c.context_length,
    // vLLM name
    c.max_model_len,
  );
}
```

Pair this with “emit only supported fields” when building gateway requests (e.g., if the adapter can’t classify reasoning support, omit reasoning fields entirely).