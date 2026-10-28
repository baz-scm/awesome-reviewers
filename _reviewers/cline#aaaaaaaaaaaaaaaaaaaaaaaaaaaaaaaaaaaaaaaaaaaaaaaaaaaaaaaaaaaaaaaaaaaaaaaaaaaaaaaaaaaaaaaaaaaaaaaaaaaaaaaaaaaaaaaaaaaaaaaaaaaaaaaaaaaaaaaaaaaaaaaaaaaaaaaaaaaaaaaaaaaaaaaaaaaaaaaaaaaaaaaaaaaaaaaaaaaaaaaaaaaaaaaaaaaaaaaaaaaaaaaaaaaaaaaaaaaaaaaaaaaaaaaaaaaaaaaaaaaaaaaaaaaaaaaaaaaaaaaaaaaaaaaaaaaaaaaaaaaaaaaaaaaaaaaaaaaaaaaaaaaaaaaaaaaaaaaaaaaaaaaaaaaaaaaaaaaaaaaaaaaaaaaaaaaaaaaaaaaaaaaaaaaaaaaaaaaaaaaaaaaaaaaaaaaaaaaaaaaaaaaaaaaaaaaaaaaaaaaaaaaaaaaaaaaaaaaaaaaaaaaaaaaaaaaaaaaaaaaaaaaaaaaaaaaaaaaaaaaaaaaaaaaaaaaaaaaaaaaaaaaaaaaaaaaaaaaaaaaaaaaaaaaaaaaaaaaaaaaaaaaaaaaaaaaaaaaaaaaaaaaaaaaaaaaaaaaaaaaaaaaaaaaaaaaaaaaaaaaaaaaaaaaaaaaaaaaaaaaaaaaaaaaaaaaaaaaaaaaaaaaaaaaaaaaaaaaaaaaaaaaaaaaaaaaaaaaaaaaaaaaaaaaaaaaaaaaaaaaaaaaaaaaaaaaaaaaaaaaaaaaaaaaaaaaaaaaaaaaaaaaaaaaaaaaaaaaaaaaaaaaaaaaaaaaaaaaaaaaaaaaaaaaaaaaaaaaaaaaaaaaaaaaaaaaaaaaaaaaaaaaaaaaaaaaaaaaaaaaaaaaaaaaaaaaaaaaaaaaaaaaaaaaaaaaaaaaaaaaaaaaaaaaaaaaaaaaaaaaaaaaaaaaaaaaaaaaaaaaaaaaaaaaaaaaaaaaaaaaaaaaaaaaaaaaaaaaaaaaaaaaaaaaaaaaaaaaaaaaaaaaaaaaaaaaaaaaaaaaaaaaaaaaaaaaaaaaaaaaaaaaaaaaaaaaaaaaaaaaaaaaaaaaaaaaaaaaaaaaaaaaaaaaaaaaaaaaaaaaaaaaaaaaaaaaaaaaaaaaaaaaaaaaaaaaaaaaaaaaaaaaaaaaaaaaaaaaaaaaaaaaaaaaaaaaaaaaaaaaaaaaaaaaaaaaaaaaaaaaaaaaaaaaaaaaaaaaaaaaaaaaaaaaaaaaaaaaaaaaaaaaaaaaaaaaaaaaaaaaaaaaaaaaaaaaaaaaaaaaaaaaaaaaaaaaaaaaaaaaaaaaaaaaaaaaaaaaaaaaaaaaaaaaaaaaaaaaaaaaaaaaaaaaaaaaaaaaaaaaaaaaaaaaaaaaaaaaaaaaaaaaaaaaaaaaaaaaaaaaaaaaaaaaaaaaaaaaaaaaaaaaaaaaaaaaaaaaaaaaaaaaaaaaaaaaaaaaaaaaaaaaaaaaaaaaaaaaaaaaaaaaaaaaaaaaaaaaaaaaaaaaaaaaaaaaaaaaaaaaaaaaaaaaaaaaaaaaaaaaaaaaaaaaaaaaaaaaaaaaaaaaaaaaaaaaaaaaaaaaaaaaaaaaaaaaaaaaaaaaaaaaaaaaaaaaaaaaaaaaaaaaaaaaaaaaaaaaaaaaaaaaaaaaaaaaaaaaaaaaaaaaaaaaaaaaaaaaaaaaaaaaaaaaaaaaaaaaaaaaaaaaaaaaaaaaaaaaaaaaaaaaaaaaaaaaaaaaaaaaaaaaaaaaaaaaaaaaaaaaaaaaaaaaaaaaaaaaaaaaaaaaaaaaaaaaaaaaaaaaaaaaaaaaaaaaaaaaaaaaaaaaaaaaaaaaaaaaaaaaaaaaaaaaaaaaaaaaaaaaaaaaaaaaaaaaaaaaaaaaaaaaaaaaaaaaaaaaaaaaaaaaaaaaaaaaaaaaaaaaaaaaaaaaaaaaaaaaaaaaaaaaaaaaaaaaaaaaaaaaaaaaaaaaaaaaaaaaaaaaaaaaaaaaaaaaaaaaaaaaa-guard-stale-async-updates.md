---
title: Guard stale async updates
description: Async work (network fetches, file reads, directory listings, repository/branch
  lookups, session creation) can resolve after the state that triggered it has moved
  on — the user signed out, switched accounts, cleared the chat, picked a different
  repo, or started a newer refresh. Without protection, a late response silently overwrites
  fresher state, reattaches...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TSX
comments_count: 10
repository_stars: 70965
---

Async work (network fetches, file reads, directory listings, repository/branch lookups, session creation) can resolve after the state that triggered it has moved on — the user signed out, switched accounts, cleared the chat, picked a different repo, or started a newer refresh. Without protection, a late response silently overwrites fresher state, reattaches a stale session, or duplicates a side effect.

Apply these two patterns consistently:

1. **Generation/request counters for state writes.** Before starting an async operation, capture the current generation/request id from a ref. Any action that invalidates in-flight work (sign-out, selection change, cache clear, account switch) bumps that counter. After the await resolves, compare the captured value against the current counter and only apply the result (write state) if it still matches; otherwise discard it. Scope the counter as narrowly as possible (e.g., per cache key/path) rather than globally, so unrelated concurrent operations aren't needlessly cancelled.

```ts
const generationRef = useRef(0);

async function refresh() {
  const generation = ++generationRef.current;
  const result = await fetchData();
  if (generation !== generationRef.current) return; // superseded, discard
  setState(result);
}

function invalidate() {
  generationRef.current++; // any later-landing response is now stale
}
```

2. **In-flight guards for user-triggered actions.** When an action can be re-triggered concurrently (double-click, repeated paste, overlapping submit), use a single ref-backed "in-flight" flag shared across all entry points that can fire it, so a second trigger while the first is still pending is a no-op (or queues) rather than duplicating the effect. Prefer resolving ordering explicitly (e.g., awaiting a shared pending promise) over relying on debouncing alone.

Favor fixing the underlying cause where possible (e.g., storing only user choices and re-deriving derived state deterministically from current inputs) over patching every stale-write site individually — but where async ordering genuinely can't be avoided, the generation-counter/in-flight-guard pattern above is the required safety net. Add a regression test that holds a stale async call open, lets a newer one complete, then resolves the stale one and asserts the fresher state wins.