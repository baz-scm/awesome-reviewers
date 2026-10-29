---
title: Validate untrusted external input
description: Treat any data that originates outside the application's trust boundary—URL/route
  params, HTTP headers, and caller-supplied option objects—as untrusted until it is
  explicitly validated or the trust relationship is configured. Do not use raw external
  values directly as object keys, flags, or configuration overrides, since this can
  lead to prototype...
repository: expressjs/Express
label: Security
language: JavaScript
comments_count: 3
repository_stars: 69579
---

Treat any data that originates outside the application's trust boundary—URL/route params, HTTP headers, and caller-supplied option objects—as untrusted until it is explicitly validated or the trust relationship is configured. Do not use raw external values directly as object keys, flags, or configuration overrides, since this can lead to prototype pollution, unintended property access, spoofed data, or bypassed security defaults.

Apply this by:
- Validating and normalizing identifiers before using them to index into objects/collections (e.g., ensure a route param is numeric and use `Object.prototype.hasOwnProperty.call()` before lookup, or coerce with `Number.parseInt()`), rather than trusting the raw string as a key.
- Never implicitly trusting client-controlled headers (e.g., `X-Forwarded-For`) unless the application has been explicitly configured to trust the proxy (e.g., only populate `req.ips` when `trust proxy` is enabled).
- When merging caller-supplied options with security-relevant defaults (e.g., cookie `expires`/`maxAge`), apply the security-critical values *after* the merge so they cannot be silently overridden by the caller:

```js
// Enforce cookie expiration regardless of caller-supplied options
var opts = merge({ path: '/' }, options);
opts.expires = new Date(1); // force expiration
opts.maxAge = 0;            // ensure modern browsers also expire immediately
```

Review any code path that accepts external input and feeds it into object lookups, header-derived logic, or option merging, and add explicit validation or ordering to close these gaps before merging.