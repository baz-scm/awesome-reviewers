---
title: Async state race guards
description: 'Async operations (fetches, creates, refreshes) can resolve out of order
  or after the state they were started for has changed, letting a stale result overwrite
  fresher state. Guard every async write with a mechanism that detects and drops stale
  results:'
repository: 'cline/cline

  '
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70942
---

Async operations (fetches, creates, refreshes) can resolve out of order or after the state they were started for has changed, letting a stale result overwrite fresher state. Guard every async write with a mechanism that detects and drops stale results:

1. **Generation/version counters**: capture a counter (or the relevant key/id) before starting the async call, bump it whenever the context changes (sign-out, reset, cache invalidation, a newer request for the same key), and re-check it immediately before writing state when the call resolves. If it no longer matches, discard the result instead of applying it.

```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current++;
  // ...clear state
}

async function loadOverview() {
  const generation = generationRef.current;
  const data = await fetchMe();
  if (generation !== generationRef.current) return; // stale, discard
  applyAccountUser(data);
}
```

This pattern applies per-key when multiple independent async reads can race (e.g. per-path directory listings, per-session creation), not just globally.

2. **In-flight guards for de-duplication**: when the same action can be triggered multiple times concurrently (double-click, repeated keypress, overlapping polls), share a single ref/promise that short-circuits re-entrant calls while one is pending, rather than letting both run and both write.

3. **Prefer eliminating the race over guarding it**: where possible, restructure so the async result is only ever a cached read feeding a pure derivation (not a direct state write), so an out-of-order response can't corrupt authoritative state at all. Reserve generation/in-flight guards for cases where a direct async write is unavoidable.

Whenever reviewing code with `await` followed by a state-setting call, ask "what happens if the user/system changes context before this resolves?" and add the appropriate guard. Add a regression test that holds a stale response, triggers the context change, then resolves the stale call and asserts it was dropped.