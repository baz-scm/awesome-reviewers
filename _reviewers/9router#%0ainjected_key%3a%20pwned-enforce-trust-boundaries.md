---
title: Enforce trust boundaries
description: Treat every point where data crosses from an untrusted source (upstream
  providers, client-supplied tool names, stored credentials) into a response or into
  privileged logic as a security boundary, and defend it explicitly rather than assuming
  good behavior.
repository: decolua/9router#%0Ainjected_key%3A%20pwned
label: Security
language: JavaScript
comments_count: 4
repository_stars: 31638
---

Treat every point where data crosses from an untrusted source (upstream providers, client-supplied tool names, stored credentials) into a response or into privileged logic as a security boundary, and defend it explicitly rather than assuming good behavior.

Apply these rules:
- Never leak secrets in responses. Sensitive fields (API keys, session tokens, provider credentials) must be stripped from any API response payload even if an alternate credential mechanism exists; keep them available server-side only, and add regression tests asserting they never appear in serialized output (e.g. a `toProviderConnectionResponse()` helper that always strips `sessionToken`).
- Sanitize untrusted content before it reaches the client. If you forward or reflect text originating from an external system (upstream error bodies, HTML error pages, provider responses), strip markup/tags and clamp length before including it in any user-facing message to avoid XSS:
```js
const shortMsg = stripHtmlTags(bodyText).slice(0, MAX_LEN);
streamController.handleError({ message: shortMsg, status });
```
- Respect explicit security/privacy opt-outs. Fallback, convenience, or compatibility logic must never silently override a caller's declared security scope (e.g. `external_web_access: false` must disable external rerouting entirely rather than being "helpfully" routed through an external provider).
- Guard reserved/privileged identifiers against collision with user-controlled input. Before injecting or relying on a reserved name (tool name, internal flag, special header), check whether the caller already defined something under that name and bail out/skip the rewrite if so — otherwise attacker- or client-controlled input could be executed with unintended privilege.

When reviewing code that handles credentials, cross-service responses, or any caller-configurable security setting, verify these boundaries are enforced and covered by tests.