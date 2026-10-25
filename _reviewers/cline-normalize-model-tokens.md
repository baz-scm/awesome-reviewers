---
title: Normalize Model Tokens
description: 'When integrating LLM providers, treat model limit metadata and token/usage
  accounting as *schema-variant inputs* that must be normalized into a single internal
  representation:'
repository: ClInE/cLiNe
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70838
---

When integrating LLM providers, treat model limit metadata and token/usage accounting as *schema-variant inputs* that must be normalized into a single internal representation:

- **Parse all advertised limit fields** (context window, max input, max output) with provider-specific aliases, so missing fields don’t trigger incorrect defaults.
- **Normalize reasoning token usage**: if providers report reasoning as a subset of `outputTokens` (including nested shapes like `outputTokens.reasoning`), subtract reasoning from `outputTokens` and track reasoning separately to prevent double-counting in totals/telemetry/cost.
- **Codify token-cap policy**: document whether defaults are floors vs ceilings; apply fractional uplift only as intended, then apply existing model/context clamps.
- **Avoid brittle provider-only special cases**: if a problem is caused by an adapter/library emitting wrong request/fields, prefer a shared normalization layer and/or an upstream fix rather than accumulating one-off Bedrock/provider routing logic.

Example pattern for reasoning-token normalization:
```ts
function subtractReasoningFromOutputTokens(usage: any, reasoningTokenCount: number) {
  // Covers both flat and nested provider shapes.
  const outputTokens = usage?.outputTokens?.["reasoning"] != null
    ? usage.outputTokens - reasoningTokenCount
    : usage.outputTokens - reasoningTokenCount;

  usage.outputTokens = Math.max(0, outputTokens);
  usage.reasoningTokenCount = reasoningTokenCount;
  return usage;
}
```

Codebase standard checklist:
- Every new provider/model catalog integration includes an alias list for limit fields.
- Every new usage-normalization change includes a regression test for the exact provider shape (flat + nested).
- Any provider-specific workaround is justified with a ticket pointing to an upstream/shared fix path.