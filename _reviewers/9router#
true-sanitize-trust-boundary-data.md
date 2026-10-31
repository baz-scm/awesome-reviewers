---
title: Sanitize trust boundary data
description: 'Any time data crosses a trust boundary, explicitly validate or sanitize
  it rather than passing it through unchecked. This applies in both directions:

  '
repository: 'decolua/9router#

  true'
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31736
---

Any time data crosses a trust boundary, explicitly validate or sanitize it rather than passing it through unchecked. This applies in both directions:

1. Outbound (server → client): Never include secrets, credentials, or tokens (e.g. AWS `sessionToken`) in API responses, even when they must be retained server-side for later use (e.g. signing requests). Build a dedicated response-serialization helper (e.g. `toProviderConnectionResponse()`) that strips sensitive fields, and reuse it consistently across create/list/detail/update endpoints so no code path accidentally leaks a secret. Add regression tests that assert the sensitive field is absent from every response shape.

2. Inbound (external/untrusted → client-visible): Never reflect raw content from an untrusted upstream (error pages, HTML bodies, third-party text) directly into a user-facing message. Strip markup and clamp length before surfacing it, to avoid XSS via injected scripts/tags:
```js
const bodyText = await providerResponse.text().catch(() => '');
const safeMsg = bodyText
  .replace(/<[^>]*>/g, '')   // strip tags
  .slice(0, 200);            // clamp length
```

3. Respect explicit security/privacy intent from the caller instead of silently overriding it — e.g., if a request declares a restricted scope (such as `external_web_access: false`), do not reroute it through a broader/external mechanism; fall back to default behavior unchanged.

4. Guard reserved/internal identifiers used for privileged dispatch (tool names, internal routes, special fields) against collision with client-supplied names. Check and bail out (or rename) when a client already defines something under a reserved identifier, so attacker-controlled input can never be executed in place of a trusted internal handler.

When implementing any feature that moves data across a trust boundary, ask: "What sensitive data could leak out?" and "What untrusted data could be injected in?" — then add explicit stripping/sanitization and a corresponding test for both directions.</description>
