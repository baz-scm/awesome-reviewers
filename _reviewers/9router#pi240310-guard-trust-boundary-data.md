---
title: Guard trust-boundary data
description: 'Any time data crosses a trust boundary — server to client, internal
  scope to external provider, or untrusted upstream content into a user-facing message
  — it must be explicitly validated, sanitized, or stripped before it leaves the boundary.
  Treat secrets, untrusted content, and access scopes as hostile by default:'
repository: decolua/9router#pi240310
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31756
---

Any time data crosses a trust boundary — server to client, internal scope to external provider, or untrusted upstream content into a user-facing message — it must be explicitly validated, sanitized, or stripped before it leaves the boundary. Treat secrets, untrusted content, and access scopes as hostile by default:

1. Never return credentials or secrets (API keys, session tokens, etc.) in API responses. Build a dedicated response-serialization helper (e.g. `toProviderConnectionResponse()`) that strips sensitive fields before sending data to clients, and add a regression test asserting the field is absent from every response path (create/list/detail/update).

2. Never reflect raw, untrusted upstream content (HTML pages, error bodies, third-party text) directly into client-facing messages or logs without sanitizing it first. Strip HTML/markup and clamp length before using upstream text in any error message that reaches the client, to eliminate XSS and log-injection risk:
```js
const bodyText = await providerResponse.text().catch(() => '');
const safeMsg = stripHtmlTags(bodyText).slice(0, MAX_MSG_LEN);
streamController.handleError(safeMsg, status);
```

3. Honor explicit access-scope/authorization flags on a request before rerouting or forwarding it. If a caller has restricted a feature (e.g. `external_web_access: false`), do not silently escalate scope by sending the request to an external system — disable the feature path entirely and pass the request through unmodified, with a test that locks in the behavior.

When implementing any feature that moves data across these boundaries, ask: "Could this leak a secret, inject untrusted content, or violate a declared access scope?" If yes, add explicit stripping/sanitization/scope-checks and cover them with regression tests.