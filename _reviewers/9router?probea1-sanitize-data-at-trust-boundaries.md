---
title: Sanitize data at trust boundaries
description: Treat every point where data crosses a trust boundary — secrets leaving
  the server, untrusted content entering a response, or client-supplied identifiers/flags
  influencing internal behavior — as security-sensitive and handle it explicitly rather
  than passing it through unchanged.
repository: decolua/9router?probeA1
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31730
---

Treat every point where data crosses a trust boundary — secrets leaving the server, untrusted content entering a response, or client-supplied identifiers/flags influencing internal behavior — as security-sensitive and handle it explicitly rather than passing it through unchanged.

Specifically:
- Never return credentials, tokens, or other secrets in API responses. If a value (e.g. an AWS `sessionToken`) is only needed server-side for signing requests, strip it in a single shared response-shaping helper (e.g. `toProviderConnectionResponse()`) used consistently across create, list, detail, and update endpoints, and cover this with a regression test that asserts the secret is absent from every response shape.
- Never reflect untrusted upstream or external content (HTML error pages, provider error bodies, etc.) directly into client-facing messages or logs. Strip tags/markup and clamp length before including such text in an error payload to avoid XSS:
```js
const bodyText = await providerResponse.text().catch(() => '');
const shortMsg = stripHtml(bodyText).slice(0, 200) || `Upstream returned unexpected response (${status})`;
```
- Respect explicit security/scope flags set by the caller (e.g. `external_web_access: false`) — never silently reroute or escalate a restricted request through a broader-access path; when such a flag is present, disable the rewrite entirely and pass the request through untouched.
- Guard against client-controlled identifiers colliding with reserved/internal names (tool names, callback IDs, etc.). Before injecting or trusting an internal construct, check whether the client already declared something under that reserved name and bail out (or rename) rather than letting client input be executed with internal trust.

Add unit/regression tests for each of these cases so future changes can't silently reintroduce a leak, an injection vector, or a scope bypass.</description>
</invoke>
