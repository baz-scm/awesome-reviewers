---
title: Normalize Provider Capabilities
description: When integrating LLM providers, implement a dedicated normalization layer
  that converts provider-specific model metadata, request fields, and usage token
  shapes into your single internal contract. Avoid generic fallbacks and ensure token
  semantics are consistent (especially reasoning tokens), then lock the adapter boundary
  with regression/contract tests.
repository: cline/cline#v30
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70894
---

When integrating LLM providers, implement a dedicated normalization layer that converts provider-specific model metadata, request fields, and usage token shapes into your single internal contract. Avoid generic fallbacks and ensure token semantics are consistent (especially reasoning tokens), then lock the adapter boundary with regression/contract tests.

Apply these rules:
- Parse provider model-list fields explicitly; if a provider uses a different capability key, map it (don’t fall back to a generic context window/cap).
- Normalize usage early so `outputTokens` means non-reasoning output only; if providers (or SDK adapters) nest reasoning tokens inside output token structures, subtract them and track reasoning separately.
- Map provider-specific request fields explicitly (e.g., Bedrock expects `reasoning.effort` for OpenAI-shaped models; don’t emit legacy/generic reasoning config for unrecognized IDs).
- Define token-cap math clearly (what is a floor vs ceiling), incorporate advertised model budgets, apply reasoning budgets, and clamp consistently.
- Add contract/regression tests that validate the exact request/usage shape at the adapter boundary (stub network; assert built request fields and normalization outcomes).

Example (usage normalization pattern):
```ts
function normalizeUsage({ outputTokens, reasoningTokenCount, ...rest }: {
  outputTokens: number;
  reasoningTokenCount: number;
}) {
  // Ensure outputTokens reflects non-reasoning output only.
  return {
    ...rest,
    outputTokens: Math.max(0, outputTokens - reasoningTokenCount),
    reasoningTokenCount,
  };
}
```