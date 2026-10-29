---
title: Explicit endpoint routing rules
description: When routing requests to a specific API endpoint, provider, or transport
  (based on model IDs, version strings, or connection config), prefer narrow, explicit
  matches over broad patterns, and centralize the resolution logic so it cannot drift
  between code paths.
repository: decolua/9router#MARKER9ROUTER7
label: API
language: JavaScript
comments_count: 3
repository_stars: 31644
---

When routing requests to a specific API endpoint, provider, or transport (based on model IDs, version strings, or connection config), prefer narrow, explicit matches over broad patterns, and centralize the resolution logic so it cannot drift between code paths.

- Match only what has been observed/verified. Avoid version-range regexes (e.g. `/^gpt-(5\.[5-9]|[6-9])/`) that "guess" future behavior — they risk silently stealing unrelated future IDs from the correct provider. Instead, match the specific known identifier (e.g. `gpt-5.6-luna`) and let unknown IDs keep the existing fallback until they're explicitly cataloged.
- Treat a `null`/unmatched lookup as a deliberate fallback, not an oversight. Document what the fallback resolves to and verify that changing a catalog entry (e.g. narrowing `supportedFormats`) doesn't break other models that still rely on the default path.
- Extract endpoint/URL resolution into a single shared function used by both the runtime executor and any validation/"test connection" probe, so a successful test always corresponds to the exact endpoint the router will actually call:

```js
export function resolveTarget(psd, model) {
  // single source of truth for URL + transport choice
  const responses = resolveApiType(psd) === "responses";
  return responses
    ? { url: `${endpoint}/v1/responses`, responses }
    : { url: `${endpoint}/v1/chat/completions`, responses };
}
```
- When validating connectivity via probes, interpret status codes according to the actual semantics of the endpoint being probed (e.g. a chat probe with `max_tokens:1` can legitimately 400 on a healthy deployment, while a responses probe returning 400/404 indicates a real misconfiguration). Encode these status-code rules explicitly and cover them with tests rather than relying on ad hoc checks.

Applying this standard prevents silent misrouting, keeps "test"/validation success in sync with real runtime behavior, and makes fallback behavior for unmapped identifiers an explicit, reviewable decision rather than an accident.</description>
