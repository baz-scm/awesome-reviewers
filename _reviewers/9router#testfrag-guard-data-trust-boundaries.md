---
title: Guard data trust boundaries
description: 'Treat every boundary where data crosses between trust levels (server-to-client,
  upstream-to-client, user-input-to-trusted-namespace) as a place where leakage or
  injection can happen, and defend it explicitly:'
repository: decolua/9router#testfrag
label: Security
language: JavaScript
comments_count: 4
repository_stars: 31419
---

Treat every boundary where data crosses between trust levels (server-to-client, upstream-to-client, user-input-to-trusted-namespace) as a place where leakage or injection can happen, and defend it explicitly:

1. Never echo secrets back to clients. Credentials such as AWS session tokens, API keys, or signing secrets must be stored and used server-side only. Build a dedicated response-shaping function (e.g. `toProviderConnectionResponse()`) that strips sensitive fields before the data is serialized, and apply it consistently across every endpoint that can return the object (create, list, detail, update) — a single missed path reintroduces the leak.

```js
function toProviderConnectionResponse(connection) {
  const { providerSpecificData, ...rest } = connection;
  const { sessionToken, ...safeProviderData } = providerSpecificData || {};
  // sessionToken stays server-side for request signing; never serialize it.
  return { ...rest, providerSpecificData: safeProviderData };
}
```

2. Never reflect untrusted external content (e.g. an upstream error page's HTML/text) directly into a client-facing message. Strip tags, clamp length, and otherwise sanitize before including it in any response, log line that may surface to users, or UI string, to prevent stored/reflected XSS.

3. Protect reserved/internal identifiers (tool names, route keys, flags) from collision with user- or client-supplied values. Before injecting or trusting an internally-generated identifier, check whether the caller already defined one with that name and bail out (or rename) rather than silently overwriting — otherwise attacker- or client-controlled data can be executed or trusted as if it were the system's own.

Add regression tests that assert secrets are absent from every response shape and that untrusted content can't smuggle markup or hijack reserved names.