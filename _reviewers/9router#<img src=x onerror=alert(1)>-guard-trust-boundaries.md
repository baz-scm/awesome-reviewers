---
title: Guard trust boundaries
description: 'Treat every point where data crosses a trust boundary as a security-sensitive
  operation, and handle three cases explicitly: (1) Outbound secrets — never let credentials,
  tokens, or other sensitive fields reach a client response even if they''re required
  internally. Keep them in the server-side object used for signing/auth, but strip
  them in the...'
repository: decolua/9router#<img src=x onerror=alert(1)>
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31644
---

Treat every point where data crosses a trust boundary as a security-sensitive operation, and handle three cases explicitly: (1) Outbound secrets — never let credentials, tokens, or other sensitive fields reach a client response even if they're required internally. Keep them in the server-side object used for signing/auth, but strip them in the response-mapping layer (e.g., a `toXResponse()` function) for every endpoint that returns the resource (create, list, detail, update), and add regression tests asserting the field is absent from all of them. (2) Inbound untrusted content — before reflecting any externally-sourced text (upstream error bodies, HTML pages, third-party API responses) into a client-facing message, strip markup/tags and clamp length; never pipe or echo raw untrusted content directly to the user, since it can carry XSS payloads. (3) Explicit security/scope constraints — when a caller sets a restrictive flag (e.g., `external_web_access: false`, a permission scope, or an access mode), never silently bypass or "work around" it via a fallback/alternate code path; honor the restriction by disabling the fallback entirely and passing the request through unchanged, and cover the behavior with a dedicated test. In all three cases, the guiding rule is: sensitive data only flows in the intended direction, and once a trust boundary or an explicit restriction is defined, no code path may silently violate it.