---
title: Sanitize data at trust boundaries
description: 'Treat every point where data crosses a trust boundary as a potential
  attack surface, and sanitize/validate on both the inbound and outbound sides:


  1. Never leak secrets outward. Credentials, tokens, and keys (e.g. an AWS `sessionToken`)
  must be stripped from every client-facing response path (create, list, detail, update),
  even if they are needed...'
repository: decolua/9router#probeA1
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31730
---

Treat every point where data crosses a trust boundary as a potential attack surface, and sanitize/validate on both the inbound and outbound sides:

1. Never leak secrets outward. Credentials, tokens, and keys (e.g. an AWS `sessionToken`) must be stripped from every client-facing response path (create, list, detail, update), even if they are needed server-side for signing requests. Build an explicit "to client" serializer that whitelists safe fields rather than trusting that a field was never added to the response.

2. Never forward untrusted external content verbatim. If upstream/third-party responses (HTML error pages, plain text, etc.) are reflected into error messages, logs shown in UIs, or piped to a client, strip markup/tags and clamp length before exposing them. Raw untrusted text in an error path is an XSS vector just like any other unsanitized input.

3. Never let external input silently collide with internal reserved identifiers. When a system auto-injects an internal/reserved name (e.g. a fallback tool name, admin role, internal header), always check whether the caller has already defined something with that same name before overwriting or granting it trusted behavior. If there's a collision, fail safe (skip the rewrite / reject the request) instead of letting attacker-controlled input assume privileged/internal semantics.

Example pattern to strip secrets from outbound data:
```js
function toClientResponse(connection) {
  const { sessionToken, ...safe } = connection; // never serialize sessionToken to the client
  return safe;
}
```

Add a regression test for each of these boundaries (response shape, sanitized error text, reserved-name collision) so a future refactor can't silently reintroduce the leak.