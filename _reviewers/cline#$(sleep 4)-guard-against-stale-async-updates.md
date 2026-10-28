---
title: Guard against stale async updates
description: Hooks that kick off async work (invokes, fetches, timers) must verify
  that the state they're about to update is still current before applying the result,
  and must base dependency/refresh keys on every input that can make old data stale.
  Capture a generation or epoch counter (and/or the target session/thread id) when
  the async call starts, and only dispatch...
repository: cline/cline#$(sleep 4)
label: React
language: TypeScript
comments_count: 6
repository_stars: 70978
---

Hooks that kick off async work (invokes, fetches, timers) must verify that the state they're about to update is still current before applying the result, and must base dependency/refresh keys on every input that can make old data stale. Capture a generation or epoch counter (and/or the target session/thread id) when the async call starts, and only dispatch its result if that generation/id still matches the latest one. Don't assume an async side effect succeeded — read its actual outcome (e.g. what was actually removed/attached) before updating optimistic UI state. When an operation snapshots data (like attached files) at request time but resolves later, reconcile the snapshot against the live state at resolution time rather than blindly applying either the snapshot or the current state.

Example pattern:

```ts
const generationRef = useRef(0);

async function bind(sessionId: string) {
  generationRef.current += 1;
  const generation = generationRef.current;
  const result = await invoke(sessionId);
  if (generation !** generationRef.current) return; // stale, discard
  dispatch({ type: "reply", result });
}
```

Apply this same discipline to:
- Refresh/refetch keys: include every signal that should invalidate cached data (e.g. combine run status, user-message count, and tool-call count, not just one of them), so a mutation without some of those signals doesn't get treated as still current.
- Optimistic UI reconciliation: when matching a pending action to its confirmed event (e.g. locating the just-sent message in a list), explicitly skip or account for other optimistically-inserted rows so the match isn't duplicated or misapplied.
- Undo/rollback flows: verify what state actually resulted from the original action (what was actually removed, started, or sent) before deciding how to undo it, and guard against double-invocation while an undo is in flight.

This prevents late-arriving async results, outdated refs, or stale snapshots from corrupting UI state after the user has already moved on (switched threads, started a new run, or edited further).