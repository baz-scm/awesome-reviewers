---
title: Verify provider SDK semantics
description: LLM provider integrations must not assume generic AI SDK behavior applies
  uniformly across providers and versions. Before relying on timeout resets, retry
  eligibility, usage-field shapes, or capability metadata, verify the actual runtime
  behavior of the pinned SDK/provider against real responses (e.g., confirm whether
  a first-chunk timeout only resets on...
repository: cline/cline#`sleep 4`
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70979
---

LLM provider integrations must not assume generic AI SDK behavior applies uniformly across providers and versions. Before relying on timeout resets, retry eligibility, usage-field shapes, or capability metadata, verify the actual runtime behavior of the pinned SDK/provider against real responses (e.g., confirm whether a first-chunk timeout only resets on non-empty text/reasoning deltas, whether `streamRetries` actually honors `isRetryable` in the pinned version, which context-window field a provider's model-list endpoint truly enforces at runtime, or how a provider nests reasoning-token counts inside usage). Pin these findings with wire-contract or regression tests that exercise the real adapter/response shape rather than only mocks, so future SDK bumps or provider changes surface as test failures instead of silent regressions (e.g., the Bedrock Converse wire tests asserting `additionalModelRequestFields`, or the usage test covering nested `outputTokens.reasoning`). When a provider's quirk requires bespoke handling in our code (e.g., Bedrock reasoning fields), prefer first checking if the issue belongs upstream in the shared SDK/adapter, and only add local special-casing as a last resort, clearly scoped and commented with the version/condition it addresses so it can be removed once fixed upstream.