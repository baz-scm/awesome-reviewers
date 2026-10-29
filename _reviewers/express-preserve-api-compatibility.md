---
title: Preserve API compatibility
description: 'When adding or changing public request/response methods, protect existing
  contracts and behavior instead of introducing silent breaking changes. Concretely:'
repository: Expressjs/Express
label: API
language: JavaScript
comments_count: 12
repository_stars: 69580
---

When adding or changing public request/response methods, protect existing contracts and behavior instead of introducing silent breaking changes. Concretely:

- Keep parameter types and semantics stable across versions (e.g. `cookie.expires` must stay a `Date`, not sometimes accept `0`/number; `res.status` must keep its documented numeric contract) and run any real behavior change through a deprecation cycle rather than changing it outright.
- Never mutate objects passed in by the caller (e.g. `res.links(arr)` must not `delete` properties off the caller's array elements) — copy/derive values instead.
- Respect explicit caller-supplied options over implicit defaults; an app-level setting (like `etag`) must not override an option the caller explicitly passed to the method call.
- When a new API wraps or supersedes an existing one, reuse the existing, well-tested implementation instead of re-implementing partial behavior. For example, `res.sendStatus` should delegate to `res.send`/`res.type` so headers, content-type, and chaining stay consistent, rather than calling `res.end()` directly and losing that behavior:

```js
res.sendStatus = function sendStatus(statusCode) {
  var body = http.STATUS_CODES[statusCode] || String(statusCode)

  this.statusCode = statusCode
  this.type('txt')

  return this.send(body)
}
```

- When supporting a new platform/runtime variant (e.g. HTTP/2) or a new input shape (e.g. array vs object args), make sure the new path produces output equivalent to the existing documented behavior (same property names, same return value shape) so users of the public API see no divergence between code paths. Any unavoidable incompatibility must be called out explicitly and gated behind a major version bump.</description>
</invoke>
