---
title: Provider limit precedence
description: When translating provider model-list metadata and token budgets into
  your internal representation, use provider-specific fields with an explicit precedence
  order, and preserve the intended clamp semantics (e.g., defaults as floors vs ceilings).
  Also ensure reasoning behavior is fixed in the shared adapter layer, not via accidental
  downstream assumptions.
repository: cline/cline#v9
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70868
---

When translating provider model-list metadata and token budgets into your internal representation, use provider-specific fields with an explicit precedence order, and preserve the intended clamp semantics (e.g., defaults as floors vs ceilings). Also ensure reasoning behavior is fixed in the shared adapter layer, not via accidental downstream assumptions.

Apply this by:
- Adding support for provider-specific window/limit keys (e.g., vLLM’s `max_model_len`).
- Choosing “actually served” limits over “advertised max” ceilings when both exist (e.g., LM Studio’s `loaded_context_length` over `max_context_length`).
- Defining a clear precedence chain for `contextWindow`, `maxInputTokens`, and `maxTokens` (so you don’t silently fall back to generic defaults).
- When computing `maxOutputTokens`, document and enforce whether your flat default is a floor or a ceiling; only raise caps via model-advertised budgets when that’s explicitly intended.
- If an adapter might accidentally include reasoning, fix it where the adapter formats requests (or upstream), rather than relying on downstream callers to “do the right thing.”

Example (sketch of precedence + budget floor semantics):
```ts
function resolveContextWindow(entry: Record<string, unknown>): number | undefined {
  // Prefer “served” limits when available
  const loaded = toPositiveInt(entry.loaded_context_length);
  if (loaded) return loaded;

  // vLLM naming
  const vllm = toPositiveInt(entry.max_model_len);
  if (vllm) return vllm;

  // Generic/advertised ceilings
  return toPositiveInt(
    entry.context_window,
    entry.max_context_length,
    entry.context_length,
  );
}

function resolveMaxOutputTokens({
  defaultMaxOutputTokens,
  modelMaxOutputTokens,
}: {
  defaultMaxOutputTokens?: number;
  modelMaxOutputTokens?: number;
}): number {
  const baseDefault = defaultMaxOutputTokens ?? DEFAULT_GATEWAY_MAX_OUTPUT_TOKENS;

  // Keep flat default as a floor; only raise for sufficiently large models.
  if (defaultMaxOutputTokens === undefined && isPositiveFiniteNumber(modelMaxOutputTokens)) {
    return Math.max(
      baseDefault,
      Math.floor(modelMaxOutputTokens * DEFAULT_GATEWAY_MAX_OUTPUT_FRACTION),
    );
  }

  return baseDefault;
}

function toPositiveInt(v: unknown): number | undefined {
  return typeof v === 'number' && Number.isFinite(v) && v > 0 ? Math.trunc(v) : undefined;
}
```