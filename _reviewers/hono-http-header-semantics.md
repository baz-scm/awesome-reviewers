---
title: HTTP header semantics
description: When implementing networking middleware (proxy, compress, CORS, etc.),
  handle HTTP headers according to their exact RFC semantics rather than naive string
  checks, and be deliberate about merge/overwrite order.
repository: honojs/Hono
label: Networking
language: TypeScript
comments_count: 8
repository_stars: 32741
---

When implementing networking middleware (proxy, compress, CORS, etc.), handle HTTP headers according to their exact RFC semantics rather than naive string checks, and be deliberate about merge/overwrite order.

- Parse multi-value headers (e.g. `Accept-Encoding`, `Connection`) properly: respect q-values, wildcards, case-insensitivity, and comma-separated tokens instead of using `String.includes()`, which gives false positives/negatives (e.g. matching `x-gzip` as `gzip`).
- When merging options into a base `RequestInit`/header set, be explicit about which side wins. Spread user-supplied overrides *before* setting required fields so they can't silently clobber critical values, or vice versa depending on intent — but always document and test the resulting precedence:
  ```ts
  // user-supplied requestInit must not override required fields
  const init: RequestInit = {
    ...requestInit,
    method: request.method,
    body: request.body,
    duplex: request.body ? 'half' : undefined,
    headers,
  }
  ```
- For headers that combine across requests/responses (e.g. `Vary`), merge with existing values instead of overwriting:
  ```ts
  const vary = new Set(c.res.headers.get('Vary')?.split(/\s*,\s*/) ?? [])
  vary.add('Origin')
  set('Vary', [...vary].join(', '))
  ```
- When one header changes the semantics of another (e.g. re-compressing a body invalidates `Content-Length`, or stripping `Content-Encoding` while keeping `Content-Range`), reason through RFC-defined dependencies rather than deleting/keeping headers unconditionally. Only remove/modify what is actually invalidated.
- Use header APIs that normalize names/values for you (`Headers#delete`, `Headers#has`) instead of manual case normalization, and prefer `append` vs `set` deliberately based on whether duplicate values are expected.
- Add targeted tests covering RFC edge cases (q=0, wildcard `*`, case differences, duplicate headers, compressed vs. uncompressed responses) to lock in correct behavior.