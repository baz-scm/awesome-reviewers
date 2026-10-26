---
title: Provider token budgeting
description: When building model-aware AI requests (model selection plus context/input/output
  token caps), always derive token/window limits from the provider’s effective advertised
  fields and apply well-defined fallback precedence.
repository: cline/cline#v29
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70893
---

When building model-aware AI requests (model selection plus context/input/output token caps), always derive token/window limits from the provider’s effective advertised fields and apply well-defined fallback precedence.

Rules:
1) Prefer effective runtime limits over ceilings.
   - If both “max/ceiling” and “loaded/effective” values exist, use the effective one for budgeting (so compaction and truncation happen only when the provider will actually reject).
2) Map provider-specific fields explicitly.
   - If the provider advertises different names (e.g., vLLM vs OpenAI-style), add the correct field to your model-source normalization so you don’t fall back to an incorrect generic default.
3) Use consistent default precedence and correct semantics (floor vs ceiling).
   - Caller-provided defaults must win.
   - Catalog-derived defaults should be treated as designed (e.g., a floor that can be raised by a fraction of model budget, then clamped by advertised caps/context).
4) Don’t hardcode one provider’s “last-resort” model across all providers.
   - Use provider manifest defaults when available; otherwise only then fall back to a global default.

Example (field-priority + safe fallback semantics):
```ts
// Pseudocode for normalizing provider model-list entries
function effectiveContextWindow(entry: any): number | undefined {
  // LM Studio-style: loaded_context_length is what actually serves
  if (typeof entry.loaded_context_length === "number") return entry.loaded_context_length;
  // vLLM-style: max_model_len is the context window they advertise
  if (typeof entry.max_model_len === "number") return entry.max_model_len;
  // Generic fallback names
  return entry.context_length ?? entry.context_window ?? entry.max_context_length;
}

function synthesizeMaxOutputTokens({
  callerDefault,
  modelMaxOutputTokens,
  flatFloor,
  fraction,
}: {
  callerDefault?: number;
  modelMaxOutputTokens?: number;
  flatFloor: number;
  fraction: number;
}) {
  // Caller wins
  if (callerDefault != null) return callerDefault;

  // Catalog-derived floor: only raise from flatFloor when model budget supports it
  const fractionBased =
    typeof modelMaxOutputTokens === "number"
      ? Math.floor(modelMaxOutputTokens * fraction)
      : undefined;

  const base = fractionBased != null ? Math.max(flatFloor, fractionBased) : flatFloor;
  // Later, clamp to modelMaxOutputTokens in your normal budgeting pipeline.
  return base;
}
```

Adopting this prevents subtle truncation/compaction regressions caused by wrong provider fields or overly generic defaults, and keeps token budgeting behavior stable as providers differ in how they describe model limits.