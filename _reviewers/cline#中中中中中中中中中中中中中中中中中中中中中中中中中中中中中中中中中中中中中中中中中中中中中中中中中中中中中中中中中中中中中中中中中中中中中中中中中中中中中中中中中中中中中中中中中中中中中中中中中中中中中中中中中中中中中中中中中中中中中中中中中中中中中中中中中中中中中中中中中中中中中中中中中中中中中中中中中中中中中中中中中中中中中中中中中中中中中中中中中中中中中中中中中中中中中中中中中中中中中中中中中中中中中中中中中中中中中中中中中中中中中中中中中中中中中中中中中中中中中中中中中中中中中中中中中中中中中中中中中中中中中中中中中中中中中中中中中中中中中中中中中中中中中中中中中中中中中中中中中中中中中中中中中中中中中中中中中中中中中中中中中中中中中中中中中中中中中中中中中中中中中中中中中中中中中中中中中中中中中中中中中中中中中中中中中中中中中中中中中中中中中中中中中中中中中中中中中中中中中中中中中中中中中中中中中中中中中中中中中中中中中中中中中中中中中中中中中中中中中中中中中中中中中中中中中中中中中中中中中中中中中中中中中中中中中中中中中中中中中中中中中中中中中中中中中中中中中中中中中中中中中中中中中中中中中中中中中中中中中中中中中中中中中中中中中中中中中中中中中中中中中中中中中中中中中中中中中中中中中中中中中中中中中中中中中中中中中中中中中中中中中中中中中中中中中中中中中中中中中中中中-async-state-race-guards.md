---
title: Async state race guards
description: 'Async operations (data fetches, resets, account switches, repeated user
  actions) frequently resolve out of order or after the state they were triggered
  for has already changed, letting a stale result overwrite newer state or a duplicate
  request run twice. Guard every async update that writes shared/component state with
  one of these patterns:'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70984
---

Async operations (data fetches, resets, account switches, repeated user actions) frequently resolve out of order or after the state they were triggered for has already changed, letting a stale result overwrite newer state or a duplicate request run twice. Guard every async update that writes shared/component state with one of these patterns:

1. Generation/request counters: before starting an async call, capture the current generation (or a key-scoped generation, e.g. per path/account/session). When the call resolves, only apply the result if the captured generation still matches the current one; otherwise discard it. Bump the generation whenever the underlying context changes (reset, clear, new selection, account switch) so in-flight calls started under the old context can no longer land.

```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current += 1;
  // ...clear state...
}

async function refresh() {
  const generation = generationRef.current;
  const result = await fetchStatus();
  if (generation !== generationRef.current) return; // stale, drop it
  setStatus(result);
}
```

2. In-flight dedupe: when an action can be triggered concurrently (rapid clicks, repeated paste, overlapping submits), use a ref/promise to ensure only one call is in flight at a time, and queue or ignore subsequent triggers until it settles, rather than letting two triggers race to produce duplicate effects.

Prefer resolving transient, race-prone state from the authoritative source on every read/render instead of caching a value that can be overwritten out of order — this avoids the need for extra locking entirely when the source of truth is already consistent. Only add generation/request guards where client-side state genuinely needs to persist across awaits (e.g., directory listing caches, session bindings, account-specific lookups).