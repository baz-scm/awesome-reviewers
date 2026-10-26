---
title: Provider Semantics Guardrails
description: When integrating with LLM/AI providers, treat streaming behavior, model
  metadata, reasoning support, and token accounting as provider-specific semantics
  that must be normalized and tested at the integration boundary.
repository: cline/cline#v23
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70889
---

When integrating with LLM/AI providers, treat streaming behavior, model metadata, reasoning support, and token accounting as provider-specific semantics that must be normalized and tested at the integration boundary.

Actionable rules:
- Timeout/streaming: Don’t apply a short `firstChunkMs` default that assumes early deltas. Gate it (or make it much larger) when the request/timeout isn’t explicitly set, since some hosted reasoning models may emit nothing for a while.
- Model catalog parsing: Support provider-specific metadata fields so context windows don’t silently fall back (e.g., vLLM `max_model_len` vs generic `context_length`).
- Request/adapter reasoning fields: Only send reasoning-related request fields when the adapter can reliably determine the model supports them; prefer fixing at the adapter layer (or upstream) rather than sprinkling special cases in downstream code.
- Usage/token normalization: Normalize reasoning token accounting across all known provider shapes (including nested variants like `outputTokens.reasoning`) so downstream telemetry/cost metrics don’t double-count reasoning as both “output” and “reasoning”.
- Token caps/clamps: Preserve intended semantics (e.g., whether a default is a floor vs ceiling). Document the rationale and keep existing behavior unless a conscious change is required.

Example pattern (illustrative):
```ts
// Streaming safety: only set firstChunk timer when explicitly requested
const opts: any = {};
if (timeoutMs !== undefined) {
  opts.timeout = { firstChunkMs: timeoutMs, chunkMs: timeoutMs };
}

// Usage normalization: ensure nested reasoning is subtracted
const outputTokens = Math.max(0, normalized.outputTokens - reasoningTokenCount);
return { ...normalized, outputTokens };

// Model parsing: accept provider-specific keys
const contextWindow = firstPositiveInteger(entry.context_length, entry.max_model_len);
```

Required test coverage:
- Regression tests for (a) silent-first-chunk behavior vs `firstChunkMs` aborts, (b) provider-specific model-list metadata keys, (c) reasoning request-field inclusion/exclusion, and (d) usage normalization across nested reasoning token shapes.