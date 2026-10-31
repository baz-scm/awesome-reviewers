---
title: Validate untrusted external input
description: Treat any data that originates outside your own trust boundary — upstream
  provider responses, client-supplied tool definitions, or client-declared scope flags
  — as potentially hostile, and never forward or act on it unchecked.
repository: decolua/9router#`id -u`
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31732
---

Treat any data that originates outside your own trust boundary — upstream provider responses, client-supplied tool definitions, or client-declared scope flags — as potentially hostile, and never forward or act on it unchecked.

- Sanitize before reflecting: if you must surface upstream content (e.g. an error page's `<title>` or body) back to a client, strip HTML/markup and clamp its length first. Reflecting raw upstream text into a response is an XSS vector.
  ```js
  const shortMsg = stripHtmlTags(titleMatch?.[1] ?? bodyText).slice(0, 200);
  streamController.handleError({ message: shortMsg, status });
  ```
- Honor declared security/access scopes: when a client explicitly restricts behavior (e.g. `external_web_access: false` to keep a search confined to an internal index), fallback or proxy logic must not silently broaden that scope by rerouting the request to an external provider. Detect the restriction and disable the fallback entirely rather than "fixing" it on the client's behalf.
- Guard reserved identifiers against collisions: before injecting or acting on an internal/reserved name (tool name, header, flag, etc.), check whether the client already defined something under that same name. If so, skip the rewrite/injection rather than letting your internal logic or a client-controlled definition execute in place of the other — this prevents a client from hijacking privileged internal routing or your code from accidentally running client-supplied logic as trusted.

In all three cases, add a unit test asserting the unsafe path is blocked (e.g. HTML is stripped, scope-restricted requests bypass the fallback, name collisions disable the rewrite).</description>
