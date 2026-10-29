---
title: Cache header correctness
description: 'Response objects obtained from `fetch` or the Cache API often have immutable
  headers, so caching middleware must never try to mutate them directly. Always construct
  a fresh `Response` (copying body/status/headers) before calling `.set()` or `.delete()`
  on its headers, e.g.:'
repository: honojs/hono
label: Caching
language: TypeScript
comments_count: 5
repository_stars: 32741
---

Response objects obtained from `fetch` or the Cache API often have immutable headers, so caching middleware must never try to mutate them directly. Always construct a fresh `Response` (copying body/status/headers) before calling `.set()` or `.delete()` on its headers, e.g.:

```ts
const res = new Response(c.res.clone().body, {
  status: c.res.status,
  headers: c.res.headers,
})
res.headers.set(cachedTime, String(Date.now()))
```

Failing to do this causes `TypeError: Headers are immutable` / `Can't modify immutable headers` errors in runtimes such as Deno and Cloudflare Workers.

In addition, when generating or comparing cache-related headers, follow the relevant HTTP caching RFCs precisely:
- Treat directive names (e.g. `Cache-Control: no-transform`) as case-insensitive per RFC 7234, using the `i` regex flag or lower-casing before comparison.
- Reject or normalize invalid `Vary` configurations — per RFC 7231, `Vary: *` must not be generated, since it disables caching entirely; throw a clear error if a configuration attempts this.
- Normalize `Vary` header values (dedupe and sort them, e.g. alphabetically) so that cache keys remain consistent regardless of the order directives were specified or combined with existing headers.

Applying these rules consistently prevents runtime crashes from immutable headers and avoids subtle cache-key or cache-behavior bugs caused by non-compliant header handling.