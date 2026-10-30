---
title: Normalize provider response quirks
description: LLM providers and model families report the same logical data (reasoning
  support, token usage, context-window limits, retryability, tool schema types) in
  inconsistent, provider-specific shapes. Code that routes or normalizes this data
  must enumerate the known shapes explicitly rather than assuming one canonical format,
  and must be verified against the real...
repository: cline/cline#zzz-unlikely-123abc
label: AI
language: TypeScript
comments_count: 10
repository_stars: 71035
---

LLM providers and model families report the same logical data (reasoning support, token usage, context-window limits, retryability, tool schema types) in inconsistent, provider-specific shapes. Code that routes or normalizes this data must enumerate the known shapes explicitly rather than assuming one canonical format, and must be verified against the real adapter/wire contract rather than mocked assumptions.

Concretely:
- When reading model/provider metadata (e.g. context window from a models endpoint), check every known field name providers actually use (`context_length`, `max_model_len`, etc.) instead of a subset, falling back only when none match.
- When normalizing usage, be precise about whether a field is a subset or additive (e.g. `reasoning_tokens` is part of `outputTokens` for some providers and a nested `outputTokens.reasoning` for others) — pick a single source of truth and subtract/merge consistently so downstream consumers (telemetry, cost, session totals) aren't double- or under-counting.
- When routing reasoning/thinking options or retry behavior per provider (e.g. Bedrock, Claude Code, portable AI-SDK options), prefer the SDK's documented/portable mechanism over bespoke per-provider special-casing; if a provider-specific workaround is unavoidable, require callers to pass an explicit context so the special case can't be silently bypassed by short-circuit logic.
- For retries, distinguish stream-level retries from request-level retries and only retry when the error is explicitly marked retryable; never retry after provider-owned tools/side effects have executed, and make sure telemetry spans are closed before a retry starts.
- Add wire-contract tests that exercise the real provider adapter (stubbed HTTP only) to assert on the actual request/response body for each model/provider variant (e.g. a model that can disable reasoning vs one that cannot), since subtle differences in exact-match model ids or SDK versions silently change behavior.

Example — avoid double-counting reasoning tokens that are a subset of output tokens:
```ts
// reasoning tokens are reported as part of outputTokens by most providers,
// but some nest them under outputTokens.reasoning instead.
const reasoningTokenCount = extractReasoningTokens(usage, REASONING_TOKEN_PATHS);
return {
  ...normalizedUsage,
  outputTokens: Math.max(0, normalizedUsage.outputTokens - reasoningTokenCount),
  reasoningTokenCount,
};
```
This keeps every downstream consumer in sync regardless of which provider shape produced the usage payload.