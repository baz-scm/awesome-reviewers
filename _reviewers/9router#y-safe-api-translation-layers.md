---
title: Safe API translation layers
description: 'When building compatibility/bridging code that translates, intercepts,
  or validates requests across different API surfaces (formats, providers, endpoints),
  keep the translation layer consistent and collision-safe:'
repository: decolua/9router#y
label: API
language: JavaScript
comments_count: 3
repository_stars: 31751
---

When building compatibility/bridging code that translates, intercepts, or validates requests across different API surfaces (formats, providers, endpoints), keep the translation layer consistent and collision-safe:

1. Pass through already-known request context instead of re-deriving it. If an earlier step already determined the source format, streaming mode, or target endpoint, forward that decision explicitly (e.g. `sourceFormatOverride`, `streamOverride`) rather than re-inspecting the raw body downstream — re-derivation risks disagreeing with the original decision and producing subtly wrong responses.

2. Before injecting any synthetic/reserved identifier (tool name, field, header) into a client's request, check whether the client already uses that identifier. If it does, skip the injection/rewrite entirely rather than overwriting — otherwise the system may end up executing client-supplied data as if it were its own synthetic construct:

```js
if (!toolNames.has(RESERVED_FALLBACK_TOOL_NAME)) {
  preservedTools.unshift(buildFallbackTool(tool, sourceFormat));
} // else: leave body unchanged, do not inject
```

3. When different endpoints/API variants (e.g. chat-completions vs. responses API) require different validation logic, centralize the URL/version resolution and the validity rules in one shared function used by both the live code path and any "test connection"/probe path. Explicitly enumerate which HTTP status codes count as valid, invalid, or transient (e.g. accept 2xx and known transient codes like 408/429/500/502/503/504; reject 400/401/403/404/405/410/422) so a successful probe can never represent a different outcome than the real runtime call.

Applying these rules prevents silent request/response drift, name-collision security issues, and false-positive "connection OK" states across API integrations.