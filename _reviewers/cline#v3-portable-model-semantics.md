---
title: Portable model semantics
description: When integrating multiple model providers/adapters, normalize provider-specific
  fields and token semantics into a consistent internal model—without proliferating
  provider-only special cases.
repository: cline/cline#v3
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70863
---

When integrating multiple model providers/adapters, normalize provider-specific fields and token semantics into a consistent internal model—without proliferating provider-only special cases.

Apply this standard:
- **Catalog limits:** Parse and preserve provider-specific limit fields (don’t assume one canonical name). If a provider exposes different naming, map it into a shared internal shape so defaults don’t silently degrade (e.g., vLLM `max_model_len`).
- **Reasoning accounting invariants:** Treat reasoning tokens as potentially **nested and/or a subset** of `outputTokens`. Subtract them consistently so downstream totals/telemetry aren’t double-counted.
- **Token budgeting semantics:** Define defaults as **floors/ceilings intentionally**. If a flat default is a floor, never accidentally reintroduce proportional reductions that cause truncation/retries.
- **Avoid provider special-casing:** If the adapter is the right layer, upstream/fix there rather than spreading Bedrock-vendor conditionals through your routing.
- **Regression tests:** Add tests that pin real translation shapes along the intended routing path (not just adapter-internal classification).

Example (defensive parsing + reasoning subtraction):
```ts
type ModelSourceEntry = {
  id: string;
  contextWindow?: number;
  maxInputTokens?: number;
  maxTokens?: number;
};

function firstPositiveInteger(...values: unknown[]) {
  for (const v of values) {
    if (typeof v === 'number' && Number.isFinite(v) && v > 0) return Math.trunc(v);
  }
}

function toModelSourceEntry(item: unknown): ModelSourceEntry | undefined {
  if (typeof item === 'string') {
    const id = item.trim();
    return id ? { id } : undefined;
  }
  if (!item || typeof item !== 'object' || Array.isArray(item)) return;
  const obj = item as Record<string, unknown>;
  const id = (obj.id ?? obj.name ?? obj.model);
  if (typeof id !== 'string' || !id.trim()) return;

  return {
    id: id.trim(),
    // map provider-specific limit keys
    contextWindow: firstPositiveInteger(obj.context_length, obj.contextWindow, obj.max_model_len),
    maxTokens: firstPositiveInteger(obj.maxTokens, obj.max_tokens, obj.max_model_len),
  };
}

function subtractReasoningTokens(input: {
  outputTokens: number;
  reasoningTokenCount: number;
  // some adapters/providers nest reasoning under outputTokens
  outputTokensReasoning?: number;
}) {
  const reasoning =
    input.outputTokensReasoning ?? input.reasoningTokenCount;
  return {
    outputTokens: Math.max(0, input.outputTokens - reasoning),
    reasoningTokenCount: reasoning,
  };
}
```