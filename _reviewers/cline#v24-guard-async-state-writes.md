---
title: Guard Async State Writes
description: 'For any async operation that may overlap (polling, refresh, snapshot-driven
  reads, route/org/user changes, concurrent button clicks), never write results blindly.
  Instead:'
repository: cline/cline#v24
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70891
---

For any async operation that may overlap (polling, refresh, snapshot-driven reads, route/org/user changes, concurrent button clicks), never write results blindly. Instead:

1) Use a “current request” token (generation number or cancellation token) captured at the start of the async function.
2) After every `await` (and before *any* state write), verify the token is still current.
3) Invalidate/bump tokens when starting a newer request or when the owning context changes (sign-out, switching org, cache drop).
4) If operations are per resource (file path, directory path, model/model-key), use a per-key generation map so stale responses can’t clobber fresher ones.
5) For user-triggered async side effects (e.g., clipboard reads), add an in-flight guard so repeated events can’t trigger duplicate concurrent reads that append the same data twice.

Pattern (generation per request / per key):
```ts
const genRef = useRef(0);

async function refresh() {
  const gen = ++genRef.current; // capture
  setLoading(true);
  try {
    const result = await fetchSomething();

    // guard before state writes
    if (gen !== genRef.current) return;

    setData(result);
  } finally {
    // also guard UI flags if needed
    if (gen === genRef.current) setLoading(false);
  }
}

// Example: per-key cache reads
const keyGenRef = useRef(new Map<string, number>());
function invalidateKeys(keys: string[]) {
  for (const k of keys) {
    keyGenRef.current.set(k, (keyGenRef.current.get(k) ?? 0) + 1);
  }
}

async function readKey(key: string) {
  const gen = (keyGenRef.current.get(key) ?? 0);
  const result = await readFromServer(key);
  if ((keyGenRef.current.get(key) ?? 0) !== gen) return;
  setCache(key, result);
}
```

This prevents race conditions where late/stale responses overwrite newer state, stops “double-apply” behavior, and keeps UI loading/empty states consistent under concurrency.