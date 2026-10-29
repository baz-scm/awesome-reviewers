---
title: Validate trust boundaries
description: 'Treat every point where data crosses a trust boundary as adversarial,
  and never assume client input, upstream responses, or internal identifiers are safe
  by default:'
repository: decolua/9router#testfrag
label: Security
language: JavaScript
comments_count: 6
repository_stars: 31643
---

Treat every point where data crosses a trust boundary as adversarial, and never assume client input, upstream responses, or internal identifiers are safe by default:

1. **Never leak secrets outward.** Credentials, tokens, or session secrets stored for internal use (e.g. an AWS `sessionToken` kept server-side for request signing) must be stripped from every API response (create, list, detail, update) via a single shared serializer, not re-implemented ad hoc per route. Add regression tests asserting the secret is absent from each response shape.

2. **Sanitize untrusted content before it reaches the client.** Text originating from an external/upstream source (e.g. an HTML error page proxied into a user-facing error message) must be treated as untrusted: strip markup/tags and clamp length before reflecting it back, to avoid XSS or log/response injection.

3. **Validate client-supplied input against security-relevant flags and reserved identifiers before acting on it.** Don't silently override a caller's explicit security/scope setting (e.g. rerouting a search flagged `external_web_access: false` through an external provider), and don't let client-controlled names collide with internally reserved tool/identifier names — check for collisions and bail out (leave the request unmodified) rather than risk executing attacker-controlled logic under a trusted name.

4. **Clean up security-sensitive state promptly.** Any temporary session/credential state created for an auth or login flow (e.g. an OAuth loopback session) must be closed and reaped after use or on timeout, with timers that don't keep the process alive (`.unref()`), to minimize the window an abandoned session or listener can be abused.

Whenever introducing a new API response, proxied content, or flow that stores/forwards credentials or external input, explicitly ask: what crosses the trust boundary here, and what redaction/sanitization/validation step must occur before it does?