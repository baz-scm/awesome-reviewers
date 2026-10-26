---
title: Model and Token Invariants
description: Ensure AI integrations preserve correctness by enforcing explicit invariants
  for (a) model-catalog fields, (b) reasoning-vs-output token accounting, and (c)
  max-tokens default semantics—then lock the behavior with regression tests.
repository: cline/cline#v25
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70891
---

Ensure AI integrations preserve correctness by enforcing explicit invariants for (a) model-catalog fields, (b) reasoning-vs-output token accounting, and (c) max-tokens default semantics—then lock the behavior with regression tests.

Apply these rules:
1) Use the field that matches what the model actually serves.
   - Prefer “loaded/served” limits over static “max” limits when both exist, to prevent early compaction or incorrect truncation.
2) Treat reasoning tokens as a subset of output tokens (and normalize consistently).
   - Downstream should see `outputTokens` as non-reasoning output, with reasoning tracked separately.
   - Handle nested shapes where the provider/SDK reports `outputTokens.reasoning`.
3) Respect floor vs ceiling semantics for synthesized max output.
   - If a default is intended as a *floor*, applying a fraction must never reduce small-model allowances; only “large enough” models may be lifted.
4) Make system prompt behavior mode-aware.
   - Commit/PR instructions should differ between Plan mode and action modes (e.g., only default to committing/opening PRs in act/yolo unless the user opts out).
5) Avoid brittle router-specific hacks; fix at the right layer when possible.
   - If reasoning fields are being sent incorrectly, prefer correcting the adapter/provider translation upstream, and use integration tests to pin the correct routing/portable reasoning behavior.

Minimal TypeScript example (reasoning normalization):
```ts
function subtractReasoning(outputTokens: number, reasoningTokenCount: number) {
  return Math.max(0, outputTokens - reasoningTokenCount);
}

// Also extend reasoning paths to handle nested shapes like outputTokens.reasoning.
const REASONING_TOKEN_PATHS = [
  ["reasoningTokenCount"],
  ["outputTokens", "reasoning"],
];
```

Add/maintain regression tests for:
- provider catalog shape variants (e.g., `loaded_context_length` vs `max_context_length`),
- reasoning-token reporting variants (including nested paths),
- max-token floor/ceiling behavior across small/large model caps,
- mode-specific prompt flow (Plan vs act/yolo).