---
title: Secure trust boundaries
description: 'Treat every point where server-trusted data crosses into client-facing
  responses, external upstream content, or client-controlled identifiers as a security
  boundary, and defend it explicitly:'
repository: decolua/9router#zz237855c
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31752
---

Treat every point where server-trusted data crosses into client-facing responses, external upstream content, or client-controlled identifiers as a security boundary, and defend it explicitly:

1. **Never leak secrets to clients.** Sensitive fields (API keys, session tokens, credentials) must be stripped from every outbound response path (create, list, detail, update) via a single centralized serializer, while remaining available server-side for signing/auth. Example:
```js
function toProviderConnectionResponse(connection) {
  const { sessionToken, ...safe } = connection.providerSpecificData;
  return { ...connection, providerSpecificData: safe }; // sessionToken kept only server-side
}
```

2. **Sanitize untrusted external content before reflecting it.** Upstream responses, error pages, or any third-party text must be stripped of HTML/markup and length-clamped before being surfaced in client-facing error messages, to prevent XSS via reflected content.

3. **Honor explicit security/privacy scoping flags.** If a client explicitly restricts a capability (e.g., `external_web_access: false`), never silently reroute the request through a broader-scope path — detect the restriction and bypass the rewrite entirely rather than violating the requested boundary.

4. **Don't let untrusted input spoof trusted internal identifiers.** Before injecting or trusting an internally reserved name/tool/identifier, check whether client-supplied data already claims that name; if so, skip the rewrite/injection rather than risk executing attacker-controlled logic under a trusted identity.

Add regression tests for each boundary (e.g., assert secrets are absent from every response shape, confirm scoped requests aren't rerouted, confirm reserved names can't be hijacked) so these protections can't silently regress.</description>
