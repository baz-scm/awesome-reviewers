---
title: Guard Against Stale Async
description: When async operations can overlap (polls, refreshes, reads with caches,
  sign-out/account switches, clipboard reads, timers), ensure only the latest/valid
  result can produce side effects.
repository: CLINE/CLINE
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70837
---

When async operations can overlap (polls, refreshes, reads with caches, sign-out/account switches, clipboard reads, timers), ensure only the latest/valid result can produce side effects.

Apply these rules:
1) Use a generation/token per async “unit” (whole request or per key/path/id). Increment/bump the token when invalidating cache, user changes context, or starting a newer request.
2) Before writing state, verify the token still matches the latest one. If it doesn’t, discard the result.
3) For caches keyed by item (file path, tab, model), keep a per-key generation map and bump only the affected keys.
4) For reads that are already in-flight, choose one of two safe behaviors:
   - Discard stale responses (simpler), or
   - Keep the response if it was already in-flight, mark it stale, and schedule exactly one follow-up read after the invalidation (prevents cancel/overwrite thrash).
5) For periodic polling, avoid endlessly superseding slow in-flight reads; skip scheduling work for keys that are still loading.
6) For user-triggered async side effects that must be idempotent (e.g., clipboard read then append), use a single in-flight guard so duplicate triggers can’t append twice.

Example pattern (per-key generation + discard stale writes):

```ts
const genRef = useRef(new Map<string, number>());

function bump(keys: Iterable<string>) {
  for (const k of keys) {
    genRef.current.set(k, (genRef.current.get(k) ?? 0) + 1);
  }
}

async function readAndApply(key: string) {
  const myGen = genRef.current.get(key) ?? 0;
  const result = await backendRead(key);

  // Discard out-of-order completion
  if ((genRef.current.get(key) ?? 0) !== myGen) return;

  setCache(prev => new Map(prev).set(key, result));
}

function invalidateForKey(key: string) {
  bump([key]);
  // next read will apply; any in-flight older read will be ignored
}
```

Also ensure UI hide/show or visibility changes reset the relevant async flags/timers so work continues (or stops) correctly when the view is restored, rather than leaving the system in a “half-run” concurrency state.