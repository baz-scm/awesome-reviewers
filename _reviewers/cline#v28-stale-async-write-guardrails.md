---
title: Stale Async Write Guardrails
description: Treat every async operation and event-driven side effect as concurrent
  with newer user actions and lifecycle changes. Ensure only the latest “generation/intent”
  is allowed to write state, and prevent duplicate side effects.
repository: cline/cline#v28
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70892
---

Treat every async operation and event-driven side effect as concurrent with newer user actions and lifecycle changes. Ensure only the latest “generation/intent” is allowed to write state, and prevent duplicate side effects.

Apply these rules:
1) Generation (or cancellation token) for async fetches
- For any async call whose result updates state, capture a token/generation when starting.
- Before applying results, confirm the token is still current.
- Bump the token on actions like Sign Out, account/org switches, or new refreshes.

Example (generation guard):
```ts
let generation = 0;

async function refresh() {
  const myGen = ++generation;
  setLoading(true);
  const result = await fetchData();
  if (myGen !== generation) return; // stale
  setState(result);
  setLoading(false);
}

function signOut() {
  ++generation;          // invalidate in-flight work
  setLoading(false);
  setState(undefined);
}
```

2) One-flight guards for async side effects (clipboard, file reads, etc.)
- When multiple triggers can start the same async read, keep a ref/flag indicating an in-flight read.
- Return early if already reading; clear the flag after completion.

3) Suspend or gate concurrent event handlers during critical flows
- If a component enters a “recording/capture” mode, suspend conflicting global handlers (and check a shared `areXSuspended()`-style flag) until the mode ends.

4) Lifecycle-safe cleanup must fully reset concurrency artifacts
- On hide/unmount/cleanup, clear timers and reset timer refs so that when the UI resumes it can re-arm pending work.

5) Prefer storing user intent, not derived/derived-writable state
- If late async lookups can overwrite user choice, store only the user’s selection and resolve derived fields from the latest state during render/evaluation.

If you consistently apply (1)-(4) and use (5) to eliminate “late overwrite” classes of bugs, you prevent race conditions, stale UI writes, and duplicate side effects across async/parallel UI flows.