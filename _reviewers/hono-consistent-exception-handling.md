---
title: Consistent exception handling
description: 'Standardize how errors are thrown, propagated, and reported across the
  codebase.


  1. Prefer `HTTPException` over manually constructed `Response` objects when signaling
  an HTTP-level error, so status codes and bodies stay consistent. When a custom body/content-type
  is needed, build the response via the `Context` (e.g. `c.text(...)`) and pass it
  through...'
repository: honojs/hono
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 32741
---

Standardize how errors are thrown, propagated, and reported across the codebase.

1. Prefer `HTTPException` over manually constructed `Response` objects when signaling an HTTP-level error, so status codes and bodies stay consistent. When a custom body/content-type is needed, build the response via the `Context` (e.g. `c.text(...)`) and pass it through `HTTPException`'s `res` option, rather than returning a raw `new Response(...)` that may lack proper headers.

```ts
// Prefer
const blockError = (c: Context): HTTPException =>
  new HTTPException(403, { res: c.text('Forbidden', 403) })

// Avoid
return new Response('Forbidden', { status: 403 })
```

2. Write clear, specific error messages. Extract reused messages into named constants (capitalized, descriptive), and when an error can have multiple valid causes/types, state them explicitly, e.g. `` `unexpected key type: CryptoKey.type is ${key.type}, expected 'private' or 'secret'` ``.

3. Never silently swallow errors. In generic error-handling wrappers, only catch the specific error types you intend to handle (e.g. `HTTPException`) and re-throw everything else. If relevant, also propagate the error onto `context.error` so downstream handlers/logging can observe it.

4. When an API accepts an optional `onError`/error-handling callback, define a sane default behavior (e.g. `console.error`) when no callback is supplied, so failures aren't silently lost, and ensure the callback's type signature matches the actual object passed at runtime (don't mix up related but distinct types like `StreamingApi` vs `SSEStreamingApi`).</description>
