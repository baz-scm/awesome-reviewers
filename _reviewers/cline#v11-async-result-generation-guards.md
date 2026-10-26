---
title: Async result generation guards
description: When async work can overlap (polls, fetches, cached reads, clipboard
  reads, timers), prevent stale/duplicate state writes by making each completion conditional
  on the request’s “currentness”.
repository: cline/cline#v11
label: Concurrency
language: TSX
comments_count: 8
repository_stars: 70871
---

When async work can overlap (polls, fetches, cached reads, clipboard reads, timers), prevent stale/duplicate state writes by making each completion conditional on the request’s “currentness”.

Apply this standard:
1) Use a monotonic generation token per async operation (global) or per entity (per file/path/model/key).
2) Capture the token at the start; after every await and right before any state update, verify the token is still current. Drop superseded responses.
3) For in-flight cached reads: if a newer snapshot arrives, mark the entry stale and run exactly one follow-up read after the in-flight one finishes, instead of letting a late response overwrite.
4) For lifecycle transitions (hide/unmount): clear timers and reset relevant flags so when the component becomes active again, pending work resumes correctly (and doesn’t duplicate).
5) For user-triggered async actions (clipboard, repeated clicks/Ctrl+V): use a single shared in-flight guard so rapid repeated triggers don’t duplicate side effects.

Example pattern (generation per key):

```ts
const genRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const k of keys) {
    genRef.current.set(k, (genRef.current.get(k) ?? 0) + 1);
  }
}

async function readSomething(key: string) {
  const gen = (genRef.current.get(key) ?? 0) + 1;
  genRef.current.set(key, gen);

  const result = await apiCall(key);

  // Guard: only apply if still current
  if (genRef.current.get(key) !== gen) return;

  setCache((c) => ({ ...c, [key]: result }));
}
```

This avoids race conditions where “older” completions land after the user/selection/state has moved on.