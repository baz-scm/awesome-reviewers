---
title: Cache header handling
description: When caching middleware reads, mutates, or compares HTTP headers (Cache-Control,
  ETag, expiration timestamps, etc.), account for header immutability and case-insensitivity.
repository: HONOJS/HONO
label: Caching
language: TypeScript
comments_count: 4
repository_stars: 32741
---

When caching middleware reads, mutates, or compares HTTP headers (Cache-Control, ETag, expiration timestamps, etc.), account for header immutability and case-insensitivity.

1. Never assume a `Response`'s headers are mutable. Responses returned from `fetch()` (and some runtime environments) have immutable `Headers`, so calling `.clone()` and then `headers.set(...)` can throw `TypeError: Headers are immutable`. If you need to add or modify headers, rebuild the response instead of mutating in place:

```ts
// Unsafe: clone() does not make headers mutable if the source was immutable
const res = c.res.clone()
res.headers.set(cachedTime, String(Date.now())) // may throw

// Safe: construct a new Response, copying status/body/headers
const res = new Response(c.res.clone().body, {
  status: c.res.status,
  headers: c.res.headers,
})
res.headers.set(cachedTime, String(Date.now()))
```
Also avoid unnecessary cloning when it isn't needed (e.g. when building a 304 response) — reuse the already-read response body/headers rather than re-cloning, since extra clones can corrupt the body in some environments.

2. HTTP header names and directive values (e.g. `Cache-Control` directives like `no-transform`, `max-age`) are case-insensitive per RFC 7234. Any regex or string comparison against directive names/values must be case-insensitive (e.g. add the `i` flag) or normalize to lowercase before comparing, otherwise functionally identical headers (`Max-Age=20` vs `max-age=20`) will be treated as different.

Applying both rules prevents runtime errors from immutable headers and avoids subtle cache-matching bugs caused by case differences in HTTP headers.</description>
