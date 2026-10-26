---
title: Centralize API format translation
description: 'When a service bridges multiple upstream API dialects (e.g., Chat Completions
  vs. Responses API) or client formats, put the conversion/resolution logic in a single
  shared function and call it from every entry and exit point, not just the common-case
  path. Divergent, duplicated logic is where bugs creep in: a fallback rewrite applied
  only in the...'
repository: decolua/9router#testfrag
label: API
language: JavaScript
comments_count: 3
repository_stars: 31419
---

When a service bridges multiple upstream API dialects (e.g., Chat Completions vs. Responses API) or client formats, put the conversion/resolution logic in a single shared function and call it from every entry and exit point, not just the common-case path. Divergent, duplicated logic is where bugs creep in: a fallback rewrite applied only in the non-streaming handler let forced-streaming upstreams bypass it and return unanswered tool calls to clients; an Azure URL/validation rule written separately for the "Test connection" probe and the real request path risked the two silently drifting apart; a Responses-to-Chat-Completions converter needed to mirror its forward counterpart's handling of truncated/partial output so `finish_reason` and `tool_calls` stayed correct.

Concretely:
- Extract endpoint/URL resolution, request shaping, and response translation into one exported function per concern (e.g., `resolveAzureTarget`, `responsesBodyToOpenAICompletion`) and reuse it everywhere that behavior is needed, including health checks, probes, and alternate transport paths (SSE vs JSON, streaming vs non-streaming).
- Enumerate all exit/entry sites for a cross-format behavior (e.g., native passthrough, chat/gemini body, SSE-converted body) and apply the shared logic at each one — don't assume one handler covers all client/provider combinations.
- Explicitly handle edge states symmetrically between forward and inverse conversions: partial/truncated output, incomplete tool calls, transient vs fatal HTTP statuses. A converter that works for the happy path but mishandles truncation can silently corrupt `finish_reason` or emit malformed tool calls.
- Add regression tests per path and edge case (e.g., both SSE sources × both client formats; both truncation reasons with partial tool output; each HTTP status class for probes) so future changes can't reintroduce the gap.