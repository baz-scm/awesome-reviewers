---
title: Normalize AI metadata
description: 'When integrating AI providers/models, treat provider catalogs and usage
  objects as inconsistent and normalize them centrally:


  - **Prefer “served” limits over advertised ceilings**: if a provider reports both
  a max/ceiling and an actual loaded/served value, use the served value to drive downstream
  behaviors (e.g., compaction readiness).'
repository: cline/cline#v19
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70885
---

When integrating AI providers/models, treat provider catalogs and usage objects as inconsistent and normalize them centrally:

- **Prefer “served” limits over advertised ceilings**: if a provider reports both a max/ceiling and an actual loaded/served value, use the served value to drive downstream behaviors (e.g., compaction readiness).
- **Normalize usage with reasoning-token correctness**: reasoning tokens are often a subset of output tokens and may appear nested (e.g., `outputTokens.reasoning`). Subtract reasoning from `outputTokens` so telemetry/session totals don’t double-count.
- **Avoid scattered provider-specific special cases**: if the root issue is “we shouldn’t be sending reasoning fields for this provider/model,” fix it at the translation/adaptor layer (ideally upstream in the AI SDK), then verify through end-to-end tests that cover resolver/catalog/portable-reasoning paths.
- **Make agent automation prompts mode-aware**: instructions about committing/pushing/opening PRs should vary by agent mode and user opt-outs (don’t apply the same automation rules to Plan vs act/yolo).

Example (usage normalization idea):
```ts
function normalizeUsage(normalizedUsage: any, reasoningTokenCount: number) {
  // Handles reasoning as a subset of outputTokens
  // and supports nested reasoning fields by routing them into reasoningTokenCount.
  return {
    ...normalizedUsage,
    outputTokens: Math.max(0, normalizedUsage.outputTokens - reasoningTokenCount),
  };
}
```

Example (model limit selection idea):
```ts
// If both exist, use the served/loaded limit.
const contextWindow = entry.loaded_context_length ?? entry.context_length ?? entry.max_context_length;
```