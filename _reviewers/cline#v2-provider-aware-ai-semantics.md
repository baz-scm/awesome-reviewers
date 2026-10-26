---
title: Provider-Aware AI Semantics
description: AI integration code must be resilient to provider/model variability in
  streaming, model catalogs, and usage shapes—avoid hardcoded defaults that assume
  uniform behavior.
repository: cline/cline#v2
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70861
---

AI integration code must be resilient to provider/model variability in streaming, model catalogs, and usage shapes—avoid hardcoded defaults that assume uniform behavior.

Apply these rules:
1) Timeouts must match streaming reality
- Don’t set a short `firstChunkMs` that assumes early deltas for hosted reasoning models.
- Prefer applying `firstChunkMs` only when explicitly configured, or default it conservatively.

Example pattern:
```ts
const hasExplicitFirstChunk = typeof firstChunkMs === "number";
const timeoutConfig = hasExplicitFirstChunk
  ? { firstChunkMs, chunkMs: timeoutMs }
  : undefined;

await streamText({
  // ...
  timeout: timeoutConfig
});
```

2) Model-list parsing must use effective limits, not just ceilings
- Add provider-specific fields when known (e.g., vLLM `max_model_len`).
- When the provider distinguishes “loaded/active” vs “maximum/ceiling”, use the effective served limit (e.g., LM Studio `loaded_context_length`).

3) Usage/token normalization must handle nested schema variants
- Treat “reasoning tokens” as a separately reported concept and ensure `outputTokens` reflects non-reasoning output.
- Support nested shapes like `outputTokens.reasoning` and add regression tests for them.

4) Reasoning-field support is model-specific; don’t leak fields
- Ensure adapters only send reasoning-related fields for models that truly support them.
- Prefer fixing the adapter upstream rather than adding fragile local special-cases, and pin behavior with adapter translation tests.

This standard reduces aborts, incorrect context budgeting, and double-counted telemetry/costs when swapping providers or updating underlying model catalogs/adapters.