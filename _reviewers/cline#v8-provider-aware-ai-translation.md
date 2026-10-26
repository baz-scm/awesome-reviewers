---
title: Provider-Aware AI Translation
description: 'When integrating with LLM providers, translate model capabilities and
  build requests defensively: don’t assume uniform field names, don’t send fields
  the provider rejects, don’t rely on generic defaults that change effective limits,
  and don’t generate message sequences that violate provider protocol invariants.'
repository: cline/cline#v8
label: AI
language: TypeScript
comments_count: 8
repository_stars: 70867
---

When integrating with LLM providers, translate model capabilities and build requests defensively: don’t assume uniform field names, don’t send fields the provider rejects, don’t rely on generic defaults that change effective limits, and don’t generate message sequences that violate provider protocol invariants.

Apply these rules:
- Map catalog/manifest fields by provider reality: prefer “actual served” limits over “advertised max” (e.g., LM Studio: use `loaded_context_length` when present).
- Support provider-specific limit field names in your model-source parsing (e.g., vLLM: consider `max_model_len`).
- Centralize capability/shape translation in the adapter/resolver layer; avoid scattered special-casing. If a provider adapter is wrong (e.g., Bedrock reasoning fields), fix it upstream rather than adding per-route hacks.
- Treat token/default math carefully: clearly distinguish floors vs ceilings and preserve existing clamps.
- Preserve message protocol invariants: when buffering/injecting context, ensure it won’t break tool-call/tool-result pairing rules; tests should verify the selected behavior for resume/edge cases.

Sketch (model-source parsing pattern):
```ts
function firstPositiveInt(...values: unknown[]): number | undefined {
  for (const v of values) {
    if (typeof v === "number" && Number.isFinite(v) && v > 0) return Math.trunc(v);
  }
}

// Prefer actual served limits when available; otherwise fall back to maxima.
function contextWindowFromCatalog(entry: Record<string, unknown>) {
  return firstPositiveInt(
    entry.loaded_context_length, // LM Studio actual capacity
    entry.max_context_length,    // LM Studio max
    entry.max_model_len,         // vLLM
    entry.context_window,
    entry.context_length,
  );
}
```

If you can’t guarantee correctness via translation and protocol-safe message construction, add focused tests for the failing edge (unsupported reasoning fields, resume with seeded tool calls, catalog-lag placeholders, etc.) and make the system explicitly reject unsupported history shapes rather than silently losing context.