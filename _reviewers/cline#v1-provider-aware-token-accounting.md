---
title: Provider-Aware Token Accounting
description: When integrating LLM providers, never assume a single schema for (a)
  model limits/capabilities or (b) usage accounting. Instead, (1) normalize provider-reported
  model metadata into one internal model, (2) derive token budgets from the *effective*
  limits the provider actually serves, and (3) normalize usage so “reasoning tokens”
  don’t double-count against...
repository: cline/cline#v1
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70862
---

When integrating LLM providers, never assume a single schema for (a) model limits/capabilities or (b) usage accounting. Instead, (1) normalize provider-reported model metadata into one internal model, (2) derive token budgets from the *effective* limits the provider actually serves, and (3) normalize usage so “reasoning tokens” don’t double-count against output tokens.

Apply this checklist:
- **Support field variants for limits**: map known provider keys (e.g., `max_model_len`) into your internal `contextWindow`/`maxTokens` fields.
- **Use effective/served limits**: when a provider distinguishes “ceiling” vs “loaded/served” (e.g., LM Studio), prefer the served value (`loaded_context_length`) if present.
- **Avoid hardcoded fallbacks**: use provider manifests / declared defaults (`defaultModelId`) and only fall back when the provider truly provides none.
- **Normalize usage shape**:
  - Treat reasoning tokens as a subset of output tokens when providers report it that way.
  - Subtract reasoning from `outputTokens` and track `reasoningTokenCount` separately.
  - Handle nested shapes (e.g., `outputTokens.reasoning`) as well as top-level reasoning fields.
- **Compute token caps with explicit semantics**: caller-specified defaults win; otherwise combine model-advertised budgets with **floor/ceiling** rules and clamps (avoid “proportional reductions” that unexpectedly change truncation/retry behavior).

Example (TypeScript-style normalization):
```ts
type NormalizedUsage = {
  inputTokens: number;
  outputTokens: number;          // non-reasoning output
  reasoningTokenCount: number;
};

function normalizeUsage(providerUsage: any): NormalizedUsage {
  // Example: reasoning may appear as a subset of outputTokens, sometimes nested.
  const outputTokens = Math.max(0, Number(providerUsage?.outputTokens ?? 0));

  const reasoningTokenCount = Math.max(
    0,
    Number(
      providerUsage?.reasoningTokenCount ??
      providerUsage?.outputTokens?.reasoning ??
      providerUsage?.completion_tokens_details?.reasoning_tokens ??
      0,
    ),
  );

  return {
    inputTokens: Math.max(0, Number(providerUsage?.inputTokens ?? 0)),
    outputTokens: Math.max(0, outputTokens - reasoningTokenCount),
    reasoningTokenCount,
  };
}
```

Following this standard prevents silent regressions like (a) falling back to generic context defaults, (b) budgeting compaction against a ceiling instead of a served limit, and (c) double-booking reasoning tokens in totals/telemetry/costs.