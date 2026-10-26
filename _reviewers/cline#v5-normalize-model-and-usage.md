---
title: Normalize model and usage
description: When integrating multiple LLM providers/adapters, treat provider responses
  (model catalogs and usage objects) as shape-variant inputs. Your code should normalize
  them in one place, then rely on consistent, test-pinned outputs everywhere else.
repository: cline/cline#v5
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70864
---

When integrating multiple LLM providers/adapters, treat provider responses (model catalogs and usage objects) as shape-variant inputs. Your code should normalize them in one place, then rely on consistent, test-pinned outputs everywhere else.

Apply this standard:
- **Model metadata mapping:** Accept that providers name the same concept differently (e.g., vLLM may report the context window as `max_model_len`). Ensure your model-source parsing maps all known field variants to a canonical structure so you don’t silently fall back to arbitrary defaults.
- **Usage normalization:** Reasoning tokens may appear in different places (including nested fields like `outputTokens.reasoning`). Normalize usage so downstream counters never double-book reasoning.
- **No scattered special-casing:** If an adapter can be corrected upstream (e.g., it is sending the wrong reasoning fields), prefer that fix. In the app/runtime, keep logic centralized and covered by regression/contract tests.
- **Test real behavior:** Add wire/contract tests that exercise the real adapter behavior and verify the final translated request/usage shapes. Keep test descriptions precise.

Example pattern (usage):
```ts
function normalizeUsage(usage: any) {
  // canonical: outputTokens = non-reasoning only; reasoning tokens tracked separately
  const reasoningTokenCount =
    getNumber(usage?.reasoningTokenCount) ??
    getNumber(usage?.outputTokens?.reasoning) ??
    0;

  return {
    ...usage,
    reasoningTokenCount,
    outputTokens: Math.max(0, (usage?.outputTokens ?? 0) - reasoningTokenCount),
  };
}
```

Outcome: consistent model context selection and accurate cost/session telemetry regardless of provider/adaptor quirks.