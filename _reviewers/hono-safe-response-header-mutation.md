---
title: Safe response header mutation
description: 'When writing caching-related middleware (cache, etag, compress), never
  assume a cloned or cached `Response` has mutable headers. Responses returned directly
  from `fetch()` or retrieved from the Cache API are immutable in many runtimes (Cloudflare
  Workers, Deno), so calling `.clone()` and then `headers.set()/delete()` will throw
  `TypeError: Headers are...'
repository: honojs/Hono
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 32741
---

When writing caching-related middleware (cache, etag, compress), never assume a cloned or cached `Response` has mutable headers. Responses returned directly from `fetch()` or retrieved from the Cache API are immutable in many runtimes (Cloudflare Workers, Deno), so calling `.clone()` and then `headers.set()/delete()` will throw `TypeError: Headers are immutable`. Instead, construct a brand-new `Response` when you need to modify headers:

```ts
const res = new Response(c.res.clone().body, {
  status: c.res.status,
  headers: c.res.headers,
})
res.headers.set(cachedTime, String(Date.now()))
```

Only create the new `Response` when mutation is actually needed (e.g. wrap the `headers.set`/`delete` call in a try/catch and fall back to constructing a new `Response` on an "immutable" `TypeError`) to avoid unnecessary overhead on the common path. Apply the same pattern when stripping/retaining headers (e.g. ETag middleware building a 304 response) — only keep headers defined by spec (`Cache-Control`, `Content-Location`, `Date`, `ETag`, `Expires`, `Vary`) and avoid re-wrapping a response unless necessary, since an extra wrap can unexpectedly empty the body in some runtimes.

Additionally, when parsing or emitting cache-related headers (`Cache-Control`, `Vary`), follow the relevant RFCs precisely:
- Directive/header-name comparisons are case-insensitive — normalize to lowercase before comparing (e.g. `no-transform` regex should use the `i` flag, and directive names should be lowercased before checking for duplicates).
- Reject or guard against invalid values, e.g. throw if `Vary` is set to `"*"` since RFC 7231 §7.1.4 disallows it for effective caching.
- Sort header directive values (e.g. `Vary`) deterministically before writing them out, so that differently-ordered equivalent values don't produce different cache keys.

Following this pattern prevents runtime crashes across different hosting environments and ensures cache behavior is spec-compliant and consistent.