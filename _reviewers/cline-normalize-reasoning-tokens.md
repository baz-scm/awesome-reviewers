---
title: Normalize reasoning tokens
description: When integrating LLM providers/adapters, treat reasoning and token budgets
  as *provider-specific data shapes* and normalize them so downstream systems don’t
  double-count or receive invalid fields.
repository: CLINE/CLINE
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70837
---

When integrating LLM providers/adapters, treat reasoning and token budgets as *provider-specific data shapes* and normalize them so downstream systems don’t double-count or receive invalid fields.

Apply these rules:
1) Normalize usage so reasoning tokens are not counted twice.
- If a provider reports reasoning as a subset of `outputTokens` (including nested shapes), subtract those reasoning tokens from `outputTokens` and track reasoning separately.

```ts
// Example pattern
const reasoningTokenCount = /* sum across configured reasoning token paths */;
const outputTokens = Math.max(0, normalizedUsage.outputTokens - reasoningTokenCount);
return {
  ...normalizedUsage,
  outputTokens,
  reasoningTokenCount,
};
```

2) Only send reasoning fields that the target backend supports.
- For models the resolver/adapter can’t classify as having reasoning support, do not emit reasoning fields that the backend rejects.

3) Map model capability fields correctly to avoid unsafe defaults.
- Prefer parsing alternate catalog field names (e.g., vLLM’s `max_model_len`) so you don’t silently fall back to an incorrect context/window.

4) Make budgeting semantics explicit.
- Treat “floor vs ceiling” intentionally (e.g., defaults as floors that may be raised by fractions, then clamped by model/context caps), and document the invariants.

5) Lock the behavior with regression tests at the integration boundary.
- Add tests for nested reasoning shapes and for “catalog lags launch” scenarios where resolution must remain stable.

This prevents cost/telemetry/session inconsistencies (double-booking), avoids invalid request payloads (backend errors), and reduces the risk of silent capability regressions caused by heterogeneous provider metadata.