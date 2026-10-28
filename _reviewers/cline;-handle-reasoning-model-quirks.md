---
title: Handle reasoning model quirks
description: 'Reasoning/thinking-capable models behave differently from plain completion
  models, and provider APIs expose those differences inconsistently. Code that talks
  to LLM providers must account for this rather than assuming a single provider''s
  behavior is universal:'
repository: cline/cline;
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70964
---

Reasoning/thinking-capable models behave differently from plain completion models, and provider APIs expose those differences inconsistently. Code that talks to LLM providers must account for this rather than assuming a single provider's behavior is universal:

- **Timeouts**: a model can think silently for a long time before streaming any text, reasoning, or tool-input deltas. Don't apply a short "first chunk" timeout derived from a general request timeout to reasoning models — a high-effort run can legitimately exceed it and get aborted as if it hung. Prefer a generous, reasoning-aware default (or only tighten it when a timeout is explicitly configured) over a one-size-fits-all value.
- **Usage accounting**: providers report reasoning tokens in different shapes (top-level `reasoning_tokens`, nested `outputTokens.reasoning`, raw provider metadata, etc.), and reasoning tokens are usually a *subset* of `outputTokens`, not additive. Normalize all known shapes into one path and subtract reasoning tokens from `outputTokens` so totals, telemetry, and billing aren't double-counted. Add a regression test per newly discovered shape.
- **State coherence**: reasoning/thinking configuration (enabled, effort level, budget tokens) must normalize to one unambiguous representation. Avoid states where "disabled" can carry an effort level, or where "not configured" is indistinguishable from an explicit low-tier choice — cover the round trip with tests.
- **Truncation recovery**: when a response is cut off at the output-token limit (common with reasoning or context-constrained local models), any retry/compaction logic must preserve already-completed provider-executed tool activity, and must classify the retry's success/failure using the exact same acceptance rules as the main run loop — don't invent a separate, looser notion of "recovered."
- **Avoid provider-specific special-casing** (e.g., Bedrock-only reasoning stripping) when a general fix is possible; if a workaround is provider-specific, document why and prefer fixing it upstream (in the SDK/provider adapter) over carrying a permanent patch in application code.

Example — stripping double-counted reasoning tokens during usage normalization:
```ts
// Providers report reasoning tokens as part of outputTokens, not additional
// to it (e.g. OpenAI's completion_tokens_details.reasoning_tokens). Strip
// them back out so outputTokens reflects true non-reasoning output.
return {
  ...normalizedUsage,
  outputTokens: Math.max(0, normalizedUsage.outputTokens - reasoningTokenCount),
};
```</description>
