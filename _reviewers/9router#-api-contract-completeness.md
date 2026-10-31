---
title: API contract completeness
description: 'Keep an API''s write path, read path, and internal dispatch logic in
  sync so the interface behaves exactly as advertised. Concretely:


  1. If server code reads a config/override field (e.g. `providerOverrides.timeoutMs`),
  the corresponding write endpoint must validate and persist that same field. Don''t
  let a normalization/sanitization layer silently drop keys...'
repository: decolua/9router#
label: API
language: JavaScript
comments_count: 3
repository_stars: 31729
---

Keep an API's write path, read path, and internal dispatch logic in sync so the interface behaves exactly as advertised. Concretely:

1. If server code reads a config/override field (e.g. `providerOverrides.timeoutMs`), the corresponding write endpoint must validate and persist that same field. Don't let a normalization/sanitization layer silently drop keys that downstream logic depends on — that creates a setting that "works" only via direct DB edits, which is confusing and unsupportable. Either extend the write endpoint's validation (e.g. `normalizeOverride` to accept `timeoutMs`/`seatBudgetMs` as finite numbers within sane bounds) or remove the read path until the API actually supports it.

2. When building routing/dispatch rules that map requests to providers or handlers (e.g. regex-based model-to-provider routing), favor the narrowest rule that solves the observed case over broad version-range wildcards. A pattern like `/^gpt-(5\.[5-9]|[6-9])/` can silently "steal" traffic from legitimately supported IDs released later. Match only the specific known identifiers, keep existing catalog/precedence rules authoritative, and add regression tests asserting both the new routing case and the untouched existing cases.

3. When translating between different request/response shapes (e.g. Responses API ↔ Chat Completions), ensure the mapping is exhaustive and correct across edge cases — partial/truncated output, multiple message items, tool calls, reasoning content — and cover these with explicit tests rather than relying on manual inspection.

In short: before shipping an API change, verify the full round trip (client write → server validation → internal consumption) is consistent, keep matching/routing logic minimally scoped, and add tests for every format/edge case your endpoint claims to support.</description>
</invoke>
