---
title: Guard stale async writes
description: Async operations (fetches, session creation, directory listings, branch
  lookups, clipboard reads) can resolve out of order or after the context that triggered
  them has already changed (a reset, sign-out, `/clear`, a new user selection). Writing
  their results unconditionally lets a stale response clobber fresher state.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70986
---

Async operations (fetches, session creation, directory listings, branch lookups, clipboard reads) can resolve out of order or after the context that triggered them has already changed (a reset, sign-out, `/clear`, a new user selection). Writing their results unconditionally lets a stale response clobber fresher state.

Standard: whenever an async result will be written back into shared/component state, capture a generation (or request id) tied to the relevant context before starting the operation, and re-check it immediately before each state write after any `await`. Bump the generation on every event that invalidates in-flight work (reset, sign-out, selection change, cache eviction). If the generation no longer matches, drop the result silently instead of applying it.

```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current += 1; // invalidate anything in flight
  setState(initial);
}

async function load() {
  const generation = generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // stale, drop it
  setState(result);
}
```

For operations that must not run concurrently or be duplicated (e.g. two rapid clipboard reads, repeated reap/init calls across remounts), use a single in-flight guard or a memoized/shared promise so a second caller awaits or no-ops on the first instead of issuing a duplicate side effect.

Where possible, prefer removing the race entirely rather than patching around it: don't cache a derived async result as separate writable state. Instead, keep only the raw user/source-of-truth inputs, and recompute the derived value fresh from current data on each use — a stale lookup then has nothing to overwrite.

Always add a regression test that starts a second (invalidating) operation while the first is still pending, resolves the first afterward, and asserts the stale result was dropped.