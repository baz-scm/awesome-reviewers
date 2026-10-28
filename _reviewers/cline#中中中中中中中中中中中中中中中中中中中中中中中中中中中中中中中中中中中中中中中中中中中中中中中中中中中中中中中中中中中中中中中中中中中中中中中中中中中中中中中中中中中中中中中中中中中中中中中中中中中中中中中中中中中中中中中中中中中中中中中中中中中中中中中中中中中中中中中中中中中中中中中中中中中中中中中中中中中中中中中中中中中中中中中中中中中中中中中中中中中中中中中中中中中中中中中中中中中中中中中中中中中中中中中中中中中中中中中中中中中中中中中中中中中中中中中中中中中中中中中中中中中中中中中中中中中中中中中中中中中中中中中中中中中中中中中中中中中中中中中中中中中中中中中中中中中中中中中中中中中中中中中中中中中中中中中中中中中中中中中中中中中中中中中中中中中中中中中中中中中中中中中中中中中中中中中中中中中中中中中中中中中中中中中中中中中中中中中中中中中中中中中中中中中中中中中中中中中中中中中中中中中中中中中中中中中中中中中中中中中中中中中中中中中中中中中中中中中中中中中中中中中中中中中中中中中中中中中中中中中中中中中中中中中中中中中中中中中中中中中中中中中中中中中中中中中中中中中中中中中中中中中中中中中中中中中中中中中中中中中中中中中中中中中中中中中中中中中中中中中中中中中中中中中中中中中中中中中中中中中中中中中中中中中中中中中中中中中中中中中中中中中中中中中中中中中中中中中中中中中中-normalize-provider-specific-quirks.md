---
title: Normalize provider-specific quirks
description: LLM providers diverge in how they report usage and accept parameters
  (e.g. reasoning tokens nested in `outputTokens` vs. reported separately, Bedrock's
  Converse API rejecting `reasoningConfig` for models without reasoning support, Azure
  vs. DeepSeek base-URL detection, per-provider default model ids). Handle this heterogeneity
  through a single, data-driven...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: AI
language: TypeScript
comments_count: 9
repository_stars: 70984
---

LLM providers diverge in how they report usage and accept parameters (e.g. reasoning tokens nested in `outputTokens` vs. reported separately, Bedrock's Converse API rejecting `reasoningConfig` for models without reasoning support, Azure vs. DeepSeek base-URL detection, per-provider default model ids). Handle this heterogeneity through a single, data-driven normalization/routing layer rather than scattering ad hoc provider-ID or base-URL string checks across call sites:

- Drive routing/eligibility decisions from model/provider capability data (catalog `defaultModelId`, advertised reasoning controls, etc.) instead of hardcoded literals or provider-name substring checks. When a provider check is genuinely required, extend the existing condition instead of duplicating/overriding it, so you don't silently drop behavior for the cases it already handled.
- Treat every known provider/response shape as a case to cover explicitly, not just the one that triggered the bug. When adding a new path to a normalization function (e.g. `REASONING_TOKEN_PATHS` in `normalizeUsage`), add a regression test pinned to that exact shape.
- For wire-level behavior (what is actually sent to/received from the provider), assert against the real request/response structure, not just that the code "ran" — e.g. test the Converse request's `additionalModelRequestFields`, not just that no error was thrown. Keep inline comments describing what is and isn't exercised precise (don't claim independence from a catalog/lookup step if a downstream resolver still consults it).
- Before adding a provider-specific workaround for a third-party SDK/adapter bug, check whether the fix belongs upstream (e.g. in the AI SDK adapter) and prefer that route when feasible; only keep local special-casing when upstream isn't practical, and keep it as narrow and well-documented as possible (cite the tracking issue).

Example of normalizing a reasoning-tokens shape discovered late:
```ts
// REASONING_TOKEN_PATHS must list every known location a provider might put
// reasoning tokens, not just the one bug report that prompted this change.
REASONING_TOKEN_PATHS.push(["outputTokens", "reasoning"]); // AI SDK v4 shape
// + regression test: "subtracts AI SDK v4's nested outputTokens.reasoning from outputTokens"
```