---
title: Sanitize untrusted external data
description: Treat any content originating from upstream providers, third-party APIs,
  or client-supplied flags as untrusted, and never forward or reflect it verbatim
  into responses, logs, or other services.
repository: decolua/9router#MARKER9ROUTER7
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31644
---

Treat any content originating from upstream providers, third-party APIs, or client-supplied flags as untrusted, and never forward or reflect it verbatim into responses, logs, or other services.

- When upstream error bodies (e.g. HTML error pages, plain-text responses) must be surfaced to the client, strip markup and clamp length before reflecting them, to prevent XSS via injected tags/scripts:
```js
function sanitizeUpstreamMessage(bodyText, maxLen = 200) {
  const noTags = bodyText.replace(/<[^>]*>/g, '').trim();
  return noTags.length > maxLen ? noTags.slice(0, maxLen) + '…' : noTags;
}
```
  Pass the result through a dedicated error handler (e.g. `streamController.handleError(...)`) rather than embedding raw strings in the client payload.
- Honor explicit security/privacy scoping flags from the request instead of silently rerouting or escalating access. For example, if a tool is scoped with `external_web_access: false`, do not reroute it through an external provider that would exfiltrate data outside the requested boundary — disable the fallback entirely and pass the request through unchanged.
- Consolidate security-sensitive logic such as credential/token refresh into a single shared implementation. Duplicated auth flows (same endpoint, header format, token-unwrap logic) are prone to drifting out of sync, and a security fix applied to one copy may silently fail to protect the other path.

Add unit tests covering the sanitization/scoping behavior (e.g., verifying HTML is stripped, verifying scoped requests are never rerouted) so these protections aren't regressed by future changes.