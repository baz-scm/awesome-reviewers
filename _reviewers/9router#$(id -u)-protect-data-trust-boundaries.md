---
title: Protect data trust boundaries
description: 'Treat every boundary between trusted and untrusted/external systems
  as a security checkpoint, both for data going out and data coming in.


  1. Never leak secrets in API responses. Credentials, tokens, and session secrets
  that must be retained server-side for signing or auth should be stripped from every
  response path (create, list, detail, update) before...'
repository: decolua/9router#$(id -u)
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31730
---

Treat every boundary between trusted and untrusted/external systems as a security checkpoint, both for data going out and data coming in.

1. Never leak secrets in API responses. Credentials, tokens, and session secrets that must be retained server-side for signing or auth should be stripped from every response path (create, list, detail, update) before serialization. Build an explicit response-shaping function rather than relying on callers to remember to omit fields:
```js
function toProviderConnectionResponse(connection) {
  const { sessionToken, ...safe } = connection; // never serialize sessionToken
  return safe;
}
```

2. Sanitize untrusted external content before it is reflected back to a client. If upstream/third-party responses (HTML error pages, raw text, etc.) are surfaced in error messages or UI, strip markup/tags and clamp length to prevent XSS or log/response injection:
```js
const shortMsg = stripHtml(bodyText).slice(0, 200) || `Upstream returned non-SSE response (${contentType})`;
```

3. Honor explicit security/privacy scope flags end-to-end; never silently reroute or widen scope. If a caller sets a restriction such as `external_web_access: false`, do not fall back to an external provider or any mechanism that would bypass the stated boundary — disable the feature entirely for that request rather than violating the constraint.

When reviewing code, check: (a) are secrets/tokens filtered out of every outbound response shape, (b) is any externally-sourced content sanitized/length-limited before being shown to users, and (c) does the code respect security/scope flags instead of working around them. Add regression tests that assert secrets are absent from responses and that scope-restricted requests never hit an external path.</description>
</invoke>
