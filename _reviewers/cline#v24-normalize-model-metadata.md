---
title: Normalize Model Metadata
description: When integrating LLM providers/adapters, treat model limits and token
  accounting as “capability-dependent data” that must be normalized to the effective
  values your system actually uses.
repository: cline/cline#v24
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70891
---

When integrating LLM providers/adapters, treat model limits and token accounting as “capability-dependent data” that must be normalized to the effective values your system actually uses.

Apply these rules:
1) Use the effective runtime fields
- If a provider exposes both a theoretical ceiling and an actually-served limit, prefer the served/loaded value (e.g., choose `loaded_context_length` over `max_context_length` for LM Studio when present) so downstream behaviors (like compaction/trim timing) trigger at the right moment.

2) Normalize usage so tokens aren’t double-counted
- Providers/adapters differ in how they report reasoning. Implement normalization that subtracts reasoning tokens from `outputTokens` and tracks reasoning separately, including variant/nested shapes.
- Add regression tests for the exact usage shapes you receive.

Example (reasoning token normalization):
```ts
function normalizeUsage(rawUsage: any): { outputTokens: number; reasoningTokenCount: number } {
  const reasoningTokenCount =
    // common shapes
    rawUsage?.reasoningTokenCount ??
    // nested AI SDK v4 shape: outputTokens.reasoning
    rawUsage?.outputTokens?.reasoning ??
    0;

  const outputTokens = Math.max(0, (rawUsage?.outputTokens ?? 0) - reasoningTokenCount);

  return { outputTokens, reasoningTokenCount };
}
```

3) Keep prompt/workflow instructions mode-aware
- If agent mode changes behavior (e.g., Plan vs act/yolo), the system prompt and task instructions must change accordingly.

4) Avoid brittle provider-specific hacks
- If behavior depends on adapter request/response shapes (e.g., Bedrock reasoning fields), prefer a portable capability-driven approach; when local special-casing is required, strongly consider upstreaming the fix to the shared AI adapter so local routing code doesn’t accumulate one-off logic.

This standard reduces subtle correctness bugs: wrong context-limit selection, double-booked token metrics/costs, and brittle adapter/request shaping across providers and model catalogs.