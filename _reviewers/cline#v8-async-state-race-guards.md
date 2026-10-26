---
title: Async state race guards
description: When you start an async operation (fetch, RPC, clipboard read, timer-based
  flush, polling), assume it may finish out of order or after the UI/user state has
  changed. Never write results into shared/UI state unless you can prove the result
  is still the latest for that logical key.
repository: cline/cline#v8
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70867
---

When you start an async operation (fetch, RPC, clipboard read, timer-based flush, polling), assume it may finish out of order or after the UI/user state has changed. Never write results into shared/UI state unless you can prove the result is still the latest for that logical key.

Apply these rules:
1) Add a per-operation *token* (generation/requestId/key) and drop stale completions.
- Example pattern (generation/requestId):
  - Increment/store a token when starting.
  - After every await (before setState), check the token is still current.
  - If not current, return without writing.

2) Don’t capture state for later writes across awaits.
- If persistence/state depends on “current selection/user”, use a state updater or ref that reads the latest value at commit time.

3) Guard against duplicate triggers that can cause repeated side effects.
- Use an in-flight ref/lock for event handlers that can be invoked rapidly (e.g., right/middle click + Ctrl+V) so only one clipboard read/appended side effect runs at a time.

4) On hide/unmount during Activity-style visibility, cleanup must reset async-driving state.
- Cancel timers/recording/flush logic and reset flags to a consistent baseline so re-show re-arms correctly.

Minimal illustrative example (token + current-state update):
```ts
const opIdRef = useRef(0);
const persistRef = useRef(latestSelection);

async function loadAndCommit() {
  const opId = ++opIdRef.current;
  const result = await doAsync();

  if (opId !== opIdRef.current) return; // stale

  const current = persistRef.current; // latest selection
  if (!current) return;

  setState(prev => ({ ...prev, value: result }));
}

function onVisibilityHideCleanup() {
  clearTimeout(timerRef.current);
  timerRef.current = null;
  setIsListening(false);
  setIsProcessing(false);
}
```

Outcome: fewer “last write wins” race bugs, correct behavior after Sign Out / account switches / out-of-order responses, and no duplicate side effects from rapid user input.