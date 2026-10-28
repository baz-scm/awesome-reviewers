---
title: Stale async write guards
description: Any async operation (fetch, create, resolve) whose result is applied
  to shared/component state can be overtaken by a later action — a reset, sign-out,
  cancel, new selection, or a second concurrent call — and land after that newer action
  has already changed context. If the result is still applied, it silently overwrites
  newer state with stale data...
repository: cline/cline?ref=main
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70980
---

Any async operation (fetch, create, resolve) whose result is applied to shared/component state can be overtaken by a later action — a reset, sign-out, cancel, new selection, or a second concurrent call — and land after that newer action has already changed context. If the result is still applied, it silently overwrites newer state with stale data (reattaching a cleared session, reviving a signed-out user, showing an old directory listing, flipping a target selection back).

Guard every async write with a monotonically increasing generation/request token:
1. Capture the current generation (or a unique request id) before starting the async call.
2. Increment the generation on any action that invalidates in-flight work (reset, sign-out, cancel, new request for the same resource).
3. Immediately before writing state after each `await`, compare the captured generation/id to the current one; if it no longer matches, drop the result instead of applying it.

```ts
const generationRef = useRef(0);

function invalidate() {
  generationRef.current++;
}

async function load() {
  const generation = generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) {
    return; // superseded — discard
  }
  applyResult(result);
}
```

When concurrent calls must also be serialized rather than just de-duplicated (e.g. multiple prompts hitting a sandbox that is still starting), queue them so each waits for the prior one to be accepted before dispatching, instead of racing independent calls.

Where possible, prefer removing the race entirely: don't let an async lookup be the thing that writes authoritative state. Keep writes synchronous and tied directly to user actions, and treat async lookups as reads that are recomputed from current source data (e.g., resolve a selection from the latest account/workspace state on every render) rather than one-shot values cached into state. This avoids needing a generation guard at all and eliminates the whole class of "late result flips state back" bugs. Add a regression test that resolves a stale/delayed call after the invalidating action and asserts the stale result was not applied.