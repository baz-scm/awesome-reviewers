---
title: Cache invalidation correctness
description: 'Ensure cached async data can’t be corrupted by out-of-order responses,
  and avoid unnecessary reloads of stable values.


  Apply two rules:

  1) Don’t re-fetch stable config on refresh'
repository: cline/cline#v27
label: Caching
language: TSX
comments_count: 3
repository_stars: 70892
---

Ensure cached async data can’t be corrupted by out-of-order responses, and avoid unnecessary reloads of stable values.

Apply two rules:
1) Don’t re-fetch stable config on refresh
- If a value is fixed for the app/account/session lifetime after the first successful lookup, resolve it once; retry only when the initial lookup fails.

2) For snapshot-driven caches, use stale-while-revalidate with generation guards
- When you invalidate/dropping a cache entry, bump a per-key “generation” and/or mark the entry as `stale`.
- If a request is already in flight, don’t clear its eventual response blindly—either:
  - discard it if its generation is superseded, or
  - allow it to render but schedule exactly one follow-up read if it was marked stale.
- This prevents late responses from overwriting fresh data and avoids duplicate network calls.

Pattern (simplified):
```ts
const generationRef = useRef(new Map<string, number>());
const invalidate = (keys: Iterable<string>) => {
  for (const k of keys) {
    generationRef.current.set(k, (generationRef.current.get(k) ?? 0) + 1);
  }
};

async function readWithGuard(key: string, fetcher: () => Promise<any>) {
  const gen = generationRef.current.get(key) ?? 0;
  const data = await fetcher();
  const latestGen = generationRef.current.get(key) ?? 0;
  if (gen !== latestGen) return; // superseded: discard
  // set cache
}
```

Testing guidance
- Add a test that keeps a read open across a refresh/poll and asserts: (a) stale/late responses don’t overwrite fresh cache, and (b) only one follow-up read is triggered when appropriate.