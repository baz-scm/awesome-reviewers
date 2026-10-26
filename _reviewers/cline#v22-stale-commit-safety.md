---
title: Stale-Commit Safety
description: Any async work that can finish after a newer user action/refresh/sign-out/visibility
  change must not “commit” stale results into React/extension state.
repository: cline/cline#v22
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70886
---

Any async work that can finish after a newer user action/refresh/sign-out/visibility change must not “commit” stale results into React/extension state.

Standard:
1) Guard every async → state write
- Use a generation/token per logical key (global or per resource like path/id).
- Capture the generation at the start of the async operation.
- After every await (or right before any state write), verify the token is still current; otherwise return without writing.

2) Invalidate guards on superseding actions
- When the user signs out, switches orgs, starts a newer refresh, changes target selection, etc., bump/advance the generation or otherwise invalidate the in-flight token.

3) On hide/unmount, fully reset schedulers
- Clear pending timers/flush refs and null out timer refs in cleanup, so when the UI becomes visible again it re-arms correctly.

4) Prefer preventing the class of bug
- If you can, avoid async-driven writes to derived selections entirely; store only user intent and re-resolve from latest state after async reads.

5) For user-triggered duplicated async actions, use an in-flight guard
- Use a shared “single-flight” callback (or ref-based lock) so repeated clicks/short bursts can’t append the same result twice.

Example pattern (generation guard):
```ts
const genRef = useRef(0);

function bumpGen() {
  genRef.current += 1;
}

async function refresh() {
  const myGen = ++genRef.current;
  setLoading(true);

  const result = await fetchSomething();
  if (genRef.current !== myGen) return; // drop stale

  setState(result);
  setLoading(false);
}

function onUserAction() {
  bumpGen(); // invalidates in-flight work
  setState(null);
}
```

Example pattern (timer reset on visibility cleanup):
- In cleanup, clearTimeout and set timer refs back to `null`, so resuming later schedules a fresh flush instead of relying on stale timers.

Adopting this standard prevents race conditions where late responses overwrite newer user intent, avoids UI starvation from cancelled in-flight work, and ensures pause/resume flows don’t stall async pipelines.