---
title: Explicit API format routing
description: 'When a service proxies or translates between multiple upstream API surfaces/versions
  (chat-completions vs. responses, dated vs. preview versions, provider-specific transports),
  make routing and conversion decisions explicit rather than relying on broad defaults
  or loose pattern matching:'
repository: decolua/9router#%0Ainjected_key%3A%20pwned
label: API
language: JavaScript
comments_count: 4
repository_stars: 31638
---

When a service proxies or translates between multiple upstream API surfaces/versions (chat-completions vs. responses, dated vs. preview versions, provider-specific transports), make routing and conversion decisions explicit rather than relying on broad defaults or loose pattern matching:

- Prefer exact, cataloged entries (model id -> supported formats, model id -> provider) over broad regexes or version-range matches that could silently capture future/unknown ids and misroute them to the wrong endpoint. If a model is uncataloged, its fallback behavior should be a deliberate, documented default — not an accidental side effect of `null` passing through to an unrelated code path.
- Centralize URL/version/transport resolution in one shared function and reuse it everywhere that logic matters (the live request path, connection "Test" buttons, validation routes) so the runtime and the health-check can never disagree about which endpoint is actually being hit:

```js
export function resolveAzureTarget(psd = {}, model = null) {
  const responses = resolveOpenAICompatibleApiType("azure", { providerSpecificData: psd }) === "responses";
  return responses
    ? { url: `${endpoint}/openai/v1/responses?api-version=preview`, deployment, responses }
    : { url: `${endpoint}/openai/deployments/${deployment}/chat/completions?api-version=${apiVersion}`, deployment, responses };
}
```

- When validating connectivity against a given surface, judge success/failure per-surface (e.g. a 400 on chat-completions can mean "healthy, bad test payload" while the same code on the responses surface means "unsupported version") and treat retryable statuses (408/429/5xx) as valid rather than hard failures.
- When converting payloads between API formats (e.g. Responses `output[]` to Chat Completions `choices[]`), handle every real-world edge case explicitly: multiple/alternating message or reasoning items, partial output on truncation, and tool calls that are incomplete — report `length`/`content_filter` instead of `tool_calls` when output was cut off, rather than assuming a clean completion.

This keeps routing and format translation predictable, prevents regressions when new models/providers are added, and ensures tests/validators reflect the exact behavior of production traffic.