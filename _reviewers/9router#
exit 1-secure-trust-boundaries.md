---
title: Secure trust boundaries
description: Treat every point where data crosses a trust boundary — server-to-client
  responses, upstream-to-client error text, and client-supplied identifiers that could
  collide with trusted internal names — as a place that needs explicit validation
  or sanitization. Strip sensitive server-side-only fields (e.g., AWS sessionToken,
  API keys) from all outward-facing...
repository: 'decolua/9router#

  exit 1'
label: Security
language: JavaScript
comments_count: 5
repository_stars: 31737
---

Treat every point where data crosses a trust boundary — server-to-client responses, upstream-to-client error text, and client-supplied identifiers that could collide with trusted internal names — as a place that needs explicit validation or sanitization. Strip sensitive server-side-only fields (e.g., AWS sessionToken, API keys) from all outward-facing responses using a single centralized serializer, even though those values must remain available internally for signing. Sanitize any text sourced from an external/upstream system (HTML, error bodies) by stripping markup/scripts and clamping length before it is reflected into a client-visible message, to prevent XSS. Honor any access-scope restriction the client declared (e.g., "no external web access") instead of silently routing the request outside that boundary. Finally, before trusting a reserved/internal identifier to drive privileged behavior (such as a special tool name), check whether client-supplied input already defines that same identifier and skip the special-casing if so, to prevent untrusted input from impersonating trusted internal logic.