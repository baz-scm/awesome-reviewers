---
title: Commit only latest async
description: When async work (promises, polling, timers, cross-handler clipboard/event
  logic) can outlive user actions or state transitions, you must prevent it from committing
  stale side effects.
repository: cline/cline#v14
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70876
---

When async work (promises, polling, timers, cross-handler clipboard/event logic) can outlive user actions or state transitions, you must prevent it from committing stale side effects.

Apply these rules:
1) Gate commits with a version/generation or request id
- Store a version in a ref (global or per key/path).
- Increment it when the relevant input changes (e.g., sign-out, target change, new selection).
- After every await, check the ref before writing state.

2) Deduplicate or serialize overlapping async side effects
- For user actions that must be ordered (e.g., create requests) use a single “pending” promise / queue.
- For idempotent side effects (e.g., clipboard reads from rapid clicks) use an in-flight guard ref so only one read can append.

3) Don’t write derived state from stale lookups
- Prefer storing user intent (what the user chose) and resolve/compute it from fresh reads.
- Avoid “lookup results” overwriting the current choice if they arrive late.

4) Reset/clear concurrency locks on lifecycle cleanup
- If you use timers/locks, ensure cleanup clears both the timer and the ref/flag so the next visibility cycle can safely re-arm work.

Example (generation + per-action commit guard)
```ts
const genRef = useRef(0);

async function load() {
  const myGen = ++genRef.current;
  const result = await fetchSomething();
  // Commit only if still the latest
  if (myGen !== genRef.current) return;
  setState(result);
}

const inFlightRef = useRef<Promise<void> | null>(null);
async function doSingleAppend(text: string) {
  if (inFlightRef.current) return; // dedupe
  inFlightRef.current = (async () => {
    const cleaned = normalize(text);
    if (!cleaned) return;
    setText(prev => prev + cleaned);
  })().finally(() => {
    inFlightRef.current = null;
  });
}
```

If you adopt these patterns consistently, you’ll eliminate the common race conditions seen in the discussed fixes: out-of-order network/polling responses, late sign-out/selection overwrites, duplicate event-driven async side effects, and stuck work after hide/show lifecycle changes.