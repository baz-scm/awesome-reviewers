---
title: Provider response normalization
description: LLM providers and local runtimes disagree on field names, nesting, and
  semantics for the same concept (context window, reasoning tokens, tool schemas,
  usable credentials), so integration code must parse defensively across the real
  variety of shapes rather than assuming one canonical format or hardcoding a single
  vendor's quirk.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: AI
language: TypeScript
comments_count: 10
repository_stars: 70965
---

LLM providers and local runtimes disagree on field names, nesting, and semantics for the same concept (context window, reasoning tokens, tool schemas, usable credentials), so integration code must parse defensively across the real variety of shapes rather than assuming one canonical format or hardcoding a single vendor's quirk.

Apply this by:
- Accepting every known field name/alias a provider's catalog uses for a value (e.g. context window as `context_length`, `max_model_len` for vLLM, or preferring a runtime's `loaded_context_length` over its static ceiling when present), falling back only when none match, so downstream budgets (compaction, pricing) aren't silently wrong.
- Treating usage/metadata fields that can appear in multiple shapes (e.g. reasoning tokens nested under `outputTokens.reasoning` vs. a top-level `reasoningTokens`) as a list of known paths to check, with a regression test per shape, instead of a single hardcoded path.
- Recursing fully into nested structures (tool schema `items`, `anyOf`/`oneOf`/`allOf` branches) when normalizing, so a fix applied at the top level isn't silently skipped one level down.
- Checking actual usability (e.g. `isProviderSettingsUsable`) rather than a narrow "has apiKey or baseUrl" check, so auth methods like IAM roles, OAuth, or local sign-ins aren't incorrectly rejected.
- Preferring a general, capability-driven branch (e.g. "is this an Anthropic-family model") over provider-specific special-casing (e.g. a Bedrock-only reasoning module), and when a quirk truly lives in a third-party adapter, consider upstreaming the fix there and pin the floor version with a wire-level test instead of carrying a permanent workaround.

Example — checking multiple known field names instead of one:
```ts
const contextWindow = firstPositiveInteger(
	entry.context_length,
	entry.context_window,
	entry.max_context_length,
	entry.max_model_len,       // vLLM
	entry.loaded_context_length, // LM Studio, prefer over static ceiling
);
```

This keeps model capability detection, token accounting, and tool-calling correct as new providers and runtimes are added, instead of degrading silently (wrong context budget, double-counted tokens, rejected tool calls, or refused valid credentials).