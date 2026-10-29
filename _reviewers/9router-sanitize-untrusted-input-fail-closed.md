---
title: Sanitize untrusted input, fail closed
description: Treat any data that originates outside your own trust boundary—upstream
  provider responses, client-supplied tool/parameter names, or unconfigured feature
  state—as potentially hostile, and default to the safest possible behavior rather
  than optimistically trusting or guessing it.
repository: Decolua/9Router
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31641
---

Treat any data that originates outside your own trust boundary—upstream provider responses, client-supplied tool/parameter names, or unconfigured feature state—as potentially hostile, and default to the safest possible behavior rather than optimistically trusting or guessing it.

1. Sanitize before reflecting: never forward raw upstream text (HTML error pages, provider bodies, etc.) into client-facing messages or logs without stripping markup and clamping length. Reflecting untrusted content verbatim is an XSS vector.
```js
const shortMsg = stripHtmlTags(rawBody).slice(0, 200);
streamController.handleError({ message: shortMsg, status });
```

2. Protect reserved/internal identifiers from collision: before relying on a reserved name (e.g., an internally-injected tool name) to route trusted, privileged logic, check whether the client has already supplied a value with that same name. If so, abort the substitution instead of overwriting—otherwise client-controlled input can impersonate and execute as a trusted internal resource.

3. Fail closed on missing configuration: features that depend on explicit user/account configuration (credentials, provider selection, etc.) must never auto-select a fallback when unconfigured. Return a clear "not configured/declined" response instead of silently picking an arbitrary provider or account, which could route data or execute actions through an unauthorized destination.

Apply this check during review: for any code path that takes external/unvalidated data and either (a) surfaces it to a user, (b) uses it to make a trust/identity decision, or (c) acts as a fallback when state is unset, confirm it sanitizes, validates for collisions, or fails closed rather than proceeding optimistically.