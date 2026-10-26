---
title: Use async generation guards
description: 'Any async flow (fetches, IPC calls, clipboard reads, long-running polls,
  timer-driven work) must prevent stale or duplicate side effects.


  Apply these rules:'
repository: cline/cline#v15
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70877
---

Any async flow (fetches, IPC calls, clipboard reads, long-running polls, timer-driven work) must prevent stale or duplicate side effects.

Apply these rules:
1) Guard out-of-order responses
- For each async operation that can overlap, associate a requestId/generation (optionally per key/path).
- Bump/increment it when starting a new request or when invalidating (e.g., sign-out, selection change).
- After every await, check the requestId/generation matches the latest; otherwise return before any state writes.

2) Commit with the latest intent
- Don’t rely on values captured before an await to decide what to write.
- Use a ref updated on render (latestSelectionRef.current = latest value) or a functional state update that reads current state.

3) Reset scheduling state on hide/unmount-like transitions
- If “hiding” unmounts effects or cancels recording/timers, cleanup must reset timer/flag refs so the next show/activation re-arms work and doesn’t leave UI in an inconsistent state.

4) Prevent duplicate event-driven side effects
- For user actions that trigger async reads/writes (clipboard, system clipboard, double-clicks), use an in-flight lock/ref.
- If already in-flight, return early; release the lock after the read completes (or after a short settling window).

Example pattern (generation guard + latest intent):
```ts
const latestIntentRef = useRef(intent);
useEffect(() => {
  latestIntentRef.current = intent;
}, [intent]);

const genRef = useRef(new Map<string, number>());
const invalidate = useCallback((key: string) => {
  genRef.current.set(key, (genRef.current.get(key) ?? 0) + 1);
}, []);

async function load(key: string) {
  const gen = (genRef.current.get(key) ?? 0) + 1;
  genRef.current.set(key, gen);

  const result = await doAsyncWork(key);

  if ((genRef.current.get(key) ?? 0) !== gen) return; // stale

  const current = latestIntentRef.current;
  setState(prev => /* write using current */ prev);
}
```

If you can’t apply one of these (e.g., you must intentionally allow stale writes), document why and add a targeted test that covers out-of-order arrival and duplicate triggers.