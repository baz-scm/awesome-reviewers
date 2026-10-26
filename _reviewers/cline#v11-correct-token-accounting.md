---
title: Correct token accounting
description: When integrating LLM providers, treat token usage and model limits as
  *provider-variant inputs* and enforce correctness centrally (adapter/shared layer),
  not ad-hoc at call sites.
repository: cline/cline#v11
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70871
---

When integrating LLM providers, treat token usage and model limits as *provider-variant inputs* and enforce correctness centrally (adapter/shared layer), not ad-hoc at call sites.

**Standard**
1. **Normalize usage with explicit semantics**: never assume reasoning is always/never part of `outputTokens`. If the provider reports reasoning separately, accumulate it into a dedicated field (e.g., `reasoningTokens`) and keep `outputTokens` aligned with the provider’s meaning.
2. **Derive model context/max tokens from the provider catalog**: accept vendor-specific fields (e.g., vLLM `max_model_len`) and avoid silent fallbacks to arbitrary defaults (like a generic 128K) when better signals exist.
3. **Preserve intended budgeting invariants**: when synthesizing max output tokens, treat explicit caller defaults as highest priority; apply documented floors; and rely on existing context/model clamps to prevent over-admission.
4. **Avoid special-casing in feature code**: if an adapter incorrectly sends/handles reasoning (e.g., Bedrock), fix it in the shared provider adapter/SDK upstream so downstream logic stays consistent.

**Example pattern (token + budgeting correctness)**
```ts
type CallUsage = {
  inputTokens: number;
  outputTokens: number;
  // keep reasoning semantics explicit
  reasoningTokens?: number;
};

function normalizeUsage(total: CallUsage | undefined, chunk: any): CallUsage {
  return {
    inputTokens: (total?.inputTokens ?? 0) + (chunk.inputTokens ?? 0),
    outputTokens: (total?.outputTokens ?? 0) + (chunk.outputTokens ?? 0),
    // Only set when the provider reports it separately
    reasoningTokens:
      (total?.reasoningTokens ?? 0) + (chunk.reasoningTokens ?? 0),
  };
}

function synthesizeMaxOutputTokens(input: {
  defaultMaxOutputTokens?: number;
  reasoningBudgetTokens?: number;
  outputReserveTokens?: number;
  model: { maxOutputTokens?: number };
}) {
  const baseDefault = input.defaultMaxOutputTokens ?? DEFAULT_GATEWAY_MAX_OUTPUT_TOKENS;

  // model-driven floor adjustment only when caller didn’t override
  const catalogDefault =
    input.defaultMaxOutputTokens === undefined &&
    isPositiveFiniteNumber(input.model.maxOutputTokens)
      ? Math.max(
          baseDefault,
          Math.floor(input.model.maxOutputTokens * DEFAULT_GATEWAY_MAX_OUTPUT_FRACTION),
        )
      : baseDefault;

  return catalogDefault + (input.reasoningBudgetTokens ? input.outputReserveTokens ?? 0 : 0);
}
```

Applying this standard reduces truncation/retry loops, prevents subtle reasoning-token/accounting bugs, and keeps provider-specific quirks contained where they belong (adapters/SDK), improving overall reliability of AI behavior.