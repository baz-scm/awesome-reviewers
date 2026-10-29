---
title: Preserve API compatibility and semantics
description: 'When adding or modifying public request/response/app methods, preserve
  their documented types, return values, and behavior unless the change is explicitly
  scoped to a major version with a deprecation path. Examples: don''t silently change
  `flatten` to `Array.prototype.flat` (different depth semantics) in a minor release,
  don''t let `cookie.expires` accept a...'
repository: expressjs/Express
label: API
language: JavaScript
comments_count: 19
repository_stars: 69579
---

When adding or modifying public request/response/app methods, preserve their documented types, return values, and behavior unless the change is explicitly scoped to a major version with a deprecation path. Examples: don't silently change `flatten` to `Array.prototype.flat` (different depth semantics) in a minor release, don't let `cookie.expires` accept a `number` when the documented type is `Date`, don't alter `req.accepts()` so it always returns `true`, and don't change `req.path` semantics between HTTP/1 and HTTP/2 without a deprecation cycle. If a behavior change is unavoidable, gate it behind a new major version or a deprecation warning, and add tests covering the old and new behavior.

Additionally, new or extended API surface should be built on top of existing, well-tested primitives rather than reimplemented from scratch, so HTTP semantics stay correct and consistent:
- `res.sendStatus()` should delegate to `res.send()` (not `res.end()`) so Content-Type, Content-Length, and other headers are set the same way as the rest of the response API:
```js
res.sendStatus = function sendStatus(statusCode) {
  var body = http.STATUS_CODES[statusCode] || String(statusCode)
  this.statusCode = statusCode
  this.type('txt')
  return this.send(body)
}
```
- Don't reuse getters/setters for a purpose they weren't designed for (e.g. `res.get`/`res.set` are header accessors and must not be used to read/write arbitrary app settings).
- Follow the relevant HTTP/W3C spec when generating headers (e.g. `Link` header attribute quoting/ordering, not injecting `charset` into a `Blob`'s `type` that the caller didn't request, respecting an already-set `Content-Type`).
- Choose HTTP verbs that match the semantics of the operation (e.g. `PUT` for full-resource replacement vs `PATCH` for partial updates), and validate/clamp inputs (status codes, lengths) according to the spec rather than accepting out-of-range or ambiguous values.

Treat any change to a public method's signature, return type, or side effects as a breaking change requiring explicit versioning, tests for both old and new behavior, and clear documentation.