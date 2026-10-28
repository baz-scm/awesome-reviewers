---
title: Guard stale async results
description: 'Whenever a component or hook kicks off async work (fetch, create, poll,
  directory read, clipboard read) and later writes state from the result, assume a
  newer action can start and finish before the old one resolves. Protect every such
  write with a guard so out-of-order completions can''t clobber fresher state:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70965
---

Whenever a component or hook kicks off async work (fetch, create, poll, directory read, clipboard read) and later writes state from the result, assume a newer action can start and finish before the old one resolves. Protect every such write with a guard so out-of-order completions can't clobber fresher state:

- Capture a generation/request token (a ref counter, or an object identity) before starting the async call. After every `await`, re-check that the token is still current before writing any state. Bump the token on any action that invalidates in-flight work (reset, sign-out, selection change, clear). If the token no longer matches, drop the result silently instead of applying it.
- Scope generations per key when multiple independent async operations can race against each other (e.g. per directory path, per model id), not just globally, so a slow request for one key doesn't get dropped because of an unrelated newer request for another key.
- Prefer not caching computed/derived async results at all when possible — store only the raw source-of-truth values and recompute the derived state fresh each time it's needed, eliminating the race entirely rather than guarding it.
- When the risk is a duplicate concurrent invocation of the *same* action (double-click, repeated paste shortcut) rather than stale ordering, use a simple in-flight boolean/ref lock that short-circuits re-entry until the pending call settles.

Example pattern:
```ts
const generationRef = useRef(0);

async function refresh() {
  const generation = ++generationRef.current;
  const result = await fetchStatus();
  if (generation !== generationRef.current) return; // a newer refresh/reset won
  setStatus(result);
}

function reset() {
  generationRef.current++; // invalidates any in-flight refresh
  setStatus(undefined);
}
```

Add a regression test that starts a slow/old async call, triggers the invalidating action, then resolves the old call and asserts state was not overwritten.