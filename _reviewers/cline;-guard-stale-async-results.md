---
title: Guard stale async results
description: 'Whenever an async operation (a fetch, poll, directory read, clipboard
  read, session creation, etc.) can be superseded by a newer trigger of the same kind
  — a user clicking again, signing out, clearing state, or an interval re-firing —
  guard against the stale result overwriting fresher state. The standard pattern is
  a generation/version counter: capture the...'
repository: cline/cline;
label: Concurrency
language: TSX
comments_count: 9
repository_stars: 70964
---

Whenever an async operation (a fetch, poll, directory read, clipboard read, session creation, etc.) can be superseded by a newer trigger of the same kind — a user clicking again, signing out, clearing state, or an interval re-firing — guard against the stale result overwriting fresher state. The standard pattern is a generation/version counter: capture the current generation in a ref before starting the async work, bump the counter whenever the relevant state is reset or invalidated (sign-out, clear, cancel, account switch), and after *every* await — before any state write — verify the captured generation still matches the current one. If it doesn't, drop the result silently instead of applying it.

```ts
const generationRef = useRef(0);

function invalidate() {
  generationRef.current++;
}

async function refresh() {
  const generation = ++generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // superseded, drop it
  setState(result);
}
```

This applies to any per-key or per-session state too (e.g. directory listings, file diffs): key the generation by the identifier being fetched, not just globally, so an in-flight request for one key isn't cancelled by an unrelated one.

Two related techniques complement this:
- When concurrent triggers should collapse into a single execution rather than racing (e.g., a cleanup routine run on every reconnect, or a clipboard read triggered by both mouse and keyboard), memoize the in-flight promise or use a single "busy" guard so duplicate triggers reuse or wait on the same operation instead of firing redundant work.
- Where feasible, eliminate the race entirely rather than reconciling it: derive state from the source of truth on every read instead of caching the result of a racy lookup for a later write, so there's nothing stale to guard against.

Add a regression test that starts an older async op, lets a newer one land first, then resolves the older one and asserts the newer result wins.