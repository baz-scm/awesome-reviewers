---
title: HTTP header spec compliance
description: When reading, writing, or forwarding HTTP headers, follow RFC semantics
  instead of naive string checks. For multi-value headers (Accept-Encoding, Vary,
  Connection, Cache-Control, etc.), parse them properly by splitting on commas, trimming
  whitespace, and handling parameters such as q-values and wildcards rather than relying
  on `.includes()` or substring...
repository: honojs/hono
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 32741
---

When reading, writing, or forwarding HTTP headers, follow RFC semantics instead of naive string checks. For multi-value headers (Accept-Encoding, Vary, Connection, Cache-Control, etc.), parse them properly by splitting on commas, trimming whitespace, and handling parameters such as q-values and wildcards rather than relying on `.includes()` or substring checks, which can produce false positives/negatives (e.g. matching `x-gzip` as `gzip`, or missing a `q=0` exclusion). When a header may already carry values (such as `Vary` or `Connection`), merge new values into the existing set instead of unconditionally overwriting it, e.g.:

```ts
const vary = new Set<string>(c.res.headers.get('Vary')?.split(/\s*,\s*/) ?? [])
vary.add('Origin')
set('Vary', [...vary].join(', '))
```

Use canonical header names as defined by the spec (e.g. `ETag`, not `Etag`), and rely on the `Headers` API's built-in case-insensitive normalization rather than manually lowercasing names before calling `get`/`set`/`delete`. When stripping or retaining headers (e.g. on 304 responses, or when proxying removes `Content-Encoding`/`Content-Length`/`Content-Range`), make sure the logic matches the actual semantics implied by the spec — for example, `Content-Length` must be dropped if the body was decompressed/changed, but headers like `Content-Range` should be preserved unless they are truly invalid for the given response. Prefer presence checks (`headers.has(...)`) over value-based checks when only existence matters. Finally, when merging configuration objects that include headers (e.g. building a `RequestInit` from both an incoming `Request` and user-supplied overrides), be explicit about spread order so that user overrides take precedence without accidentally clobbering computed values like `headers`, `body`, or `duplex`.