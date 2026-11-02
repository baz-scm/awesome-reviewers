---
title: Enforce trust boundaries
description: Treat every point where data crosses a trust boundary—secrets leaving
  the server, untrusted content entering a client-facing response, requests crossing
  between internal and external systems, or client input touching privileged internal
  identifiers—as a security-sensitive operation that must be explicitly validated
  or scrubbed.
repository: decolua/9router#zz1793619710
label: Security
language: JavaScript
comments_count: 4
repository_stars: 31855
---

Treat every point where data crosses a trust boundary—secrets leaving the server, untrusted content entering a client-facing response, requests crossing between internal and external systems, or client input touching privileged internal identifiers—as a security-sensitive operation that must be explicitly validated or scrubbed.

Concretely:
- Never return secrets or credentials (API keys, session tokens, signing material) in any response path. Strip them at the serialization boundary even if they must be retained server-side for later use (e.g. signing requests), and cover every response shape (create/list/detail/update) with tests.
```js
function toProviderConnectionResponse(record) {
  const { sessionToken, ...safe } = record; // never leaves the server
  return safe;
}
```
- Never reflect raw upstream or user-supplied content (HTML, error bodies, titles) into client-facing messages without stripping markup/scripts and clamping length — this is a direct XSS vector when the upstream is untrusted or compromised.
- When a caller explicitly restricts scope or access (e.g. `external_web_access: false`), honor that restriction end-to-end; never silently reroute or escalate the request to a broader-access path because it's convenient.
- Guard reserved/internal identifiers (tool names, route names, feature flags) against collision with client-supplied values. If a client can register something under a privileged name, check for and reject/bypass the collision instead of letting it be executed with elevated trust.

When adding any feature that forwards, logs, or displays data originating from an external or lower-trust source, explicitly identify what crosses the boundary, what must never cross it, and add a regression test asserting that boundary holds.