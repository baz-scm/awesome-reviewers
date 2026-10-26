---
title: Normalize Provider Token Usage
description: When integrating LLM providers, treat provider/model metadata and usage
  reporting as schema-variant and provider-specific. Use runtime capability fields
  (what the model actually serves), and normalize token accounting so reasoning tokens
  are never double-counted as “output”.
repository: cline/cline#v10
label: AI
language: TypeScript
comments_count: 3
repository_stars: 70869
---

When integrating LLM providers, treat provider/model metadata and usage reporting as schema-variant and provider-specific. Use runtime capability fields (what the model actually serves), and normalize token accounting so reasoning tokens are never double-counted as “output”.

Apply this standard:
- Prefer runtime limits over “advertised max” when available (e.g., use `loaded_context_length` over `max_context_length` for compaction/credit decisions).
- Normalize usage defensively across provider shapes:
  - Some providers report reasoning tokens as a subset of output (e.g., `completion_tokens_details.reasoning_tokens` or nested `outputTokens.reasoning`).
  - Subtract reasoning tokens from `outputTokens` and track reasoning separately.
- Encode adapter translation rules explicitly:
  - Only send Bedrock reasoning fields when the target model is known to support them; otherwise omit them entirely to avoid provider rejection.
- Add regression tests for the exact variant shapes you support (including nested reasoning fields and “unsupported model” branches).

Example pattern for reasoning token subtraction (handle nested and top-level shapes):
```ts
type Usage = {
  outputTokens: number;
  reasoningTokenCount?: number;
  // nested/variant shapes may appear depending on provider
  outputTokens?: { reasoning?: number } & number; // conceptual
  // ...
};

function subtractReasoningTokens(normalized: { outputTokens: number }, reasoningTokenCount: number) {
  return {
    ...normalized,
    outputTokens: Math.max(0, normalized.outputTokens - reasoningTokenCount),
  };
}
```

Net effect: fewer provider-specific regressions (rejections, bad compaction timing, and incorrect billing/telemetry) because your code consistently maps provider schemas into your internal “output vs reasoning” model.