---
title: Guard data trust boundaries
description: Treat every point where data crosses a trust boundary (server-to-client
  response, upstream-to-client error passthrough, or cross-provider routing) as a
  security checkpoint, not just a functional detail.
repository: decolua/9router#ctlA219179
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31730
---

Treat every point where data crosses a trust boundary (server-to-client response, upstream-to-client error passthrough, or cross-provider routing) as a security checkpoint, not just a functional detail.

1. Never leak secrets in outbound responses. Credentials needed server-side (e.g. signing keys, session tokens) must be stripped from any API response (create/list/detail/update) before it reaches the client, even if they must be retained internally for later use:
```js
function toProviderConnectionResponse(conn) {
  const { sessionToken, ...safe } = conn; // strip before returning to client
  return safe; // sessionToken is kept server-side only, used for signing
}
```

2. Never reflect untrusted external content (upstream HTML/error pages, provider responses, etc.) into client-facing messages without sanitizing it first. Strip HTML/script tags and clamp length before surfacing any upstream text, to prevent XSS:
```js
const shortMsg = stripHtmlTags(titleMatch?.[1] ?? bodyText).slice(0, 200);
```

3. Honor explicit client-specified security/privacy scopes throughout the request pipeline. If a client restricts a capability (e.g. `external_web_access: false`), any fallback or routing logic must respect that restriction rather than silently rerouting to an external/broader-scoped provider. When in doubt, disable the fallback and pass the request through unchanged rather than risk a scope violation.

Add regression tests for each of these cases (response shape, sanitized error text, and scope-respecting fallback behavior) so future refactors cannot reintroduce the leak, injection, or scope bypass.