---
title: Provider-Aware AI Semantics
description: When integrating with LLM/AI providers, avoid assuming uniform semantics
  for streaming, model limits, or token usage. Centralize provider-specific handling
  so behavior is correct across model types (especially hosted reasoning) and usage
  shapes.
repository: cline/cline#v12
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70872
---

When integrating with LLM/AI providers, avoid assuming uniform semantics for streaming, model limits, or token usage. Centralize provider-specific handling so behavior is correct across model types (especially hosted reasoning) and usage shapes.

Apply these rules:
1) Streaming timeouts
- Don’t set a short `firstChunkMs` by default for reasoning models. Only apply it when explicitly configured, or ensure the default is comfortably above expected “time-to-first-delta” for those providers.

Example pattern:
```ts
const isExplicit = timeoutMs !== undefined;
const timeoutConfig = isExplicit
  ? { timeout: { firstChunkMs: timeoutMs, chunkMs: timeoutMs } }
  : {};

await streamText({
  // ...
  ...(timeoutConfig as any),
});
```

2) Model window / token-limit extraction
- When parsing model-list entries, read the provider’s actual window fields and prefer the one that reflects what’s currently served.
- Examples:
  - vLLM: prefer `max_model_len` over generic fallbacks.
  - LM Studio: prefer `loaded_context_length` over `max_context_length` when present.

3) Token accounting normalization (reasoning vs output)
- Normalize usage so downstream counters don’t double-book reasoning.
- Handle all known shapes, including nested ones like `outputTokens.reasoning`, with regression tests.

Example pattern:
```ts
// after extracting reasoningTokenCount
normalizedUsage.outputTokens = Math.max(
  0,
  normalizedUsage.outputTokens - reasoningTokenCount
);
```

4) Avoid bespoke adapter sprawl
- If a provider/AI-sdk integration bug exists (e.g., sending reasoning unexpectedly), prefer fixing upstream or in the shared normalization layer rather than adding one-off special handling in multiple places.

Outcome: fewer silent regressions in production (timeouts, wrong context windows, mis-billed/over-reported usage) and a more maintainable AI integration layer.