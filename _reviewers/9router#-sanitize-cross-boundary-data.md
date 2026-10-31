---
title: Sanitize cross-boundary data
description: Any data that crosses a trust boundary — credentials going out to clients,
  upstream content being reflected back to users, or identifiers that trigger privileged
  execution — must be validated and sanitized before use, never passed through as-is.
repository: decolua/9router#
label: Security
language: JavaScript
comments_count: 4
repository_stars: 31729
---

Any data that crosses a trust boundary — credentials going out to clients, upstream content being reflected back to users, or identifiers that trigger privileged execution — must be validated and sanitized before use, never passed through as-is.

Apply this in practice:
- Never leak secrets in API responses. Build a dedicated response-shaping helper (e.g. `toProviderConnectionResponse()`) that strips sensitive fields (tokens, keys, session secrets) before returning data to the client, even though the server still needs the raw value internally.
- Treat all upstream/external content as untrusted before reflecting it to a client. If you must surface part of an upstream error body (e.g. an HTML error page's `<title>`) in a user-facing message, strip HTML/markup and clamp the length first to prevent XSS:
```js
const bodyText = await providerResponse.text().catch(() => '');
const titleMatch = bodyText.match(/<title>([^<]+)<\/title>/i);
const rawMsg = titleMatch?.[1]?.trim() || bodyText;
const safeMsg = stripHtmlTags(rawMsg).slice(0, 200);
streamController.handleError(safeMsg, status);
```
- Honor explicit security/privacy scopes set by the caller. If a request declares a restriction (e.g. `external_web_access: false`), never silently reroute it through a broader/external resource that would violate that boundary — short-circuit the feature instead of weakening the scope.
- Guard against reserved or trusted-name collisions. Before injecting or acting on an internally reserved identifier (tool name, role, flag), check whether the untrusted input already defines that identifier, and refuse/skip the operation rather than letting attacker-controlled input execute with the trust level implied by the reserved name.

In short: at every point where sensitive data leaves the server, where external content enters a response, or where trust is inferred from a name/flag, add an explicit check or sanitization step and cover it with a regression test.