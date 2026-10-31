---
title: Explicit API routing rules
description: When dispatching requests to different endpoints, transports, or providers
  (e.g. choosing `/responses` vs `/chat/completions`, or mapping a model id to a provider),
  prefer explicit, narrowly-scoped declarations over broad patterns or implicit defaults.
  A catch-all regex or a "fall back to X when unknown" rule can silently capture future/unrelated
  ids and...
repository: decolua/9router#ctl1793435320
label: API
language: JavaScript
comments_count: 3
repository_stars: 31733
---

When dispatching requests to different endpoints, transports, or providers (e.g. choosing `/responses` vs `/chat/completions`, or mapping a model id to a provider), prefer explicit, narrowly-scoped declarations over broad patterns or implicit defaults. A catch-all regex or a "fall back to X when unknown" rule can silently capture future/unrelated ids and send them to the wrong endpoint — fix the exact observed case instead of widening the match (e.g. route only the literal `gpt-5.6-luna` id to Copilot rather than a `/^gpt-(5\.[5-9]|[6-9])/` pattern that would hijack future OpenAI releases), and keep explicit catalog entries taking precedence over any fallback.

Likewise, when an API surface has multiple variants with different URL shapes or semantics (chat completions vs. the v1 responses API, different api-version requirements, etc.), centralize that resolution logic in a single shared function used by both the actual request path and any validation/health-check path (e.g. `resolveAzureTarget`), so a passing "Test Connection" can never mean a different endpoint than what the live request will hit. When validating such endpoints, be precise about which status codes indicate a real failure (auth/version/not-found) versus a transient condition (429/5xx) so probes don't give false positives or false negatives.

In short: document and encode exactly which models/ids/versions go to which endpoint, avoid speculative wildcard routing, and share one source of truth for endpoint resolution between production and validation code paths.