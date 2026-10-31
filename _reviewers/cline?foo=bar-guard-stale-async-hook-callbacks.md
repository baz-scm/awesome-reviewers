---
title: Guard stale async hook callbacks
description: Hooks that kick off async work (network calls, promises racing a timeout,
  debounced fetches) must assume the surrounding state can change before that work
  resolves — the user can navigate away, remount a pane, start a new session, or edit
  the input again. Applying a stale result as if it were still current silently corrupts
  state (overwritten drafts,...
repository: cline/cline?foo=bar
label: React
language: TypeScript
comments_count: 5
repository_stars: 71082
---

Hooks that kick off async work (network calls, promises racing a timeout, debounced fetches) must assume the surrounding state can change before that work resolves — the user can navigate away, remount a pane, start a new session, or edit the input again. Applying a stale result as if it were still current silently corrupts state (overwritten drafts, duplicated messages, stale "current" flags, files sent that were already removed).

To make async hook logic safe:
1. Snapshot the inputs/identity relevant to the operation at the moment it starts (e.g. `boundSessionId`, a `revision`, the currently-attached files, a composite refresh key that includes every dimension that can make the cached data stale — not just the obvious one).
2. Before applying the resolved result, re-validate that the captured identity still matches the live state (e.g. `if (boundRef.current !== boundSessionId) return;`). If it doesn't, discard the result instead of writing it into shared/external state.
3. When reconciling the result with current state (e.g. "which files are still attached", "is this draft still the newest one"), diff against current state rather than blindly using either the original snapshot or whatever is live when the promise settles.

Example pattern:
```ts
const boundSessionId = boundRef.current;
const snapshot = takeSnapshot();
const result = await invoke(request);
if (boundRef.current !== boundSessionId) return; // stale: a navigation/remount happened
applyResult(reconcile(snapshot, result, currentState()));
```

Apply this guard to any hook callback that awaits a promise, debounce, or race, and audit every derived boolean/key used to decide "is this data current" so it accounts for all the ways the underlying state can change (not just the common case).