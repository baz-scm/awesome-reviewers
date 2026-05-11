---
title: Deterministic Async Lifecycle
description: Ensure async features that depend on a query/promise’s lifecycle (e.g.,
  cancellation hooks, query function availability) are wired using a deterministic
  initialization order. Don’t write code paths that assume `query`/`query.promise`
  already exists; either (a) centralize initialization (e.g., reuse a prefetch-like
  path) or (b) explicitly create/transition...
repository: tanstack/query
label: Concurrency
language: JavaScript
comments_count: 2
repository_stars: 49380
---

Ensure async features that depend on a query/promise’s lifecycle (e.g., cancellation hooks, query function availability) are wired using a deterministic initialization order. Don’t write code paths that assume `query`/`query.promise` already exists; either (a) centralize initialization (e.g., reuse a prefetch-like path) or (b) explicitly create/transition query state before starting concurrent work. This prevents unreachable cancellation handles and race conditions where different callers observe different lifecycle states.

Example pattern (conceptual):
```js
async function ensureQueryInitialized({ queryHash, queryFn, client, variables }) {
  let query = client.queries.find(d => d.queryHash === queryHash)
  if (!query) {
    // Create/initialize via the single shared initialization path
    query = await client.prefetchQuery({ queryHash, queryFn, variables })
  }
  return query
}

function wireCancelAtCreation({ query, pageVariables }) {
  // Wire cancel when promises are created (when the handle is available)
  const promises = pageVariables.map(v => {
    const p = query.queryFn(v)
    // store cancel handle immediately in a dedicated field
    query._cancel = p.cancel
    return p
  })
  return Promise.all(promises)
}
```

Standard checklist:
- Define the allowed lifecycle states for `query` and `query.promise` (e.g., uninitialized → initialized → running).
- Any code needing cancellation must capture the cancel handle at the moment the promise (or equivalent control object) is created.
- Any API (like `setQueryData`) that might run before initialization must either (1) wait for a shared initialization path or (2) create the query using the same logic as other entry points.
- Add concurrency-focused tests that simulate interleavings (set before prefetch finishes, cancel before promise assignment, etc.).