---
title: HTTP header semantics
description: 'When reading, merging, or mutating HTTP headers in middleware/proxy/helper
  code, implement behavior that matches the HTTP spec rather than naive string checks.
  Concretely:'
repository: HONOJS/HONO
label: Networking
language: TypeScript
comments_count: 9
repository_stars: 32741
---

When reading, merging, or mutating HTTP headers in middleware/proxy/helper code, implement behavior that matches the HTTP spec rather than naive string checks. Concretely:

- Parse multi-value headers (e.g. `Accept-Encoding`, `Connection`) properly, honoring quality values (`q=0` means "not acceptable"), wildcards (`*`), and case-insensitive tokens, instead of using `String#includes`. For example, prefer a proper accept-parsing helper over `accepted?.includes(options.encoding)`.
- Use the `Headers` API idioms correctly: `headers.has('Content-Encoding')` instead of truthiness checks on `get`, and don't `.toLowerCase()` header names before `Headers#delete/get/set` since `Headers` already normalizes case.
- When merging/forwarding headers (proxy, CORS `Vary`, duplicate request headers), decide explicitly between `append` (to preserve multiple values) and `set` (to replace), and merge existing values instead of blindly overwriting them, e.g. union the existing `Vary` header with `Origin` rather than replacing it.
- Be careful with the order of object spreads when combining computed defaults with user-supplied `RequestInit`/options so that explicit user values win (or lose) predictably — don't let a later spread silently clobber `headers`, `method`, `body`, or `duplex`.
- Only strip/rewrite response headers like `Content-Length`/`Content-Range` when semantically required (e.g. strip `Content-Length` only if the body was recompressed; preserve `Content-Range` as-is), and verify side effects in tests (e.g. a deleted cookie must produce `Set-Cookie: name=; Max-Age=0`, not a missing header).

Add targeted tests for these edge cases (case variations, multiple headers, q-values, wildcards, overwritten options) to prevent regressions, since header-handling bugs are easy to introduce and hard to notice.