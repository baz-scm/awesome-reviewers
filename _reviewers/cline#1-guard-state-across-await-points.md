---
title: Guard state across await points
description: 'Across async code, shared mutable state (session status, bound session
  id, plugin generation, resident runtime, queued work) can change during any `await`.
  A check made just before an await, or a decision based on state read before it,
  is frequently stale by the time execution resumes — this produced the largest class
  of bugs in this codebase: teardown...'
repository: cline/cline#1
label: Concurrency
language: TypeScript
comments_count: 22
repository_stars: 71024
---

Across async code, shared mutable state (session status, bound session id, plugin generation, resident runtime, queued work) can change during any `await`. A check made just before an await, or a decision based on state read before it, is frequently stale by the time execution resumes — this produced the largest class of bugs in this codebase: teardown racing a settling turn, a stale reply applying to a session the UI has since unbound from, a replacement session being released by mistake, a rebuild racing a newer rebuild request, and more.

Treat every `await` as a point where the world can change out from under you. Apply one of these patterns rather than assuming pre-await state still holds post-await:

1. **Bump a generation/epoch counter synchronously before starting async work, and check it after every await before applying side effects.** A reply that arrives after a newer bind/start/rebuild superseded the in-flight one must be dropped.

```ts
let generation = 0;
async function bind(sessionId: string) {
  generation += 1;
  const myGeneration = generation;
  const result = await fetchSomething(sessionId);
  if (myGeneration !== generation) return; // superseded while awaiting
  apply(result);
}
```

2. **Decide and flag intent synchronously, in the same tick, before the first await**, then act on that decision after awaiting — don't re-derive the decision from state that may have moved (e.g. deciding per-session teardown path only after flagging every session, not interleaved with awaits).

3. **Re-validate the specific precondition right before mutating**, not just at entry (e.g. check `session.shuttingDown` again after `markTurnRunning`, or confirm a map entry still points at the resource you're about to release before releasing it, instead of assuming it still does because it did before the await).

4. **Serialize conflicting operations on the same resource through a single promise chain/queue/lock** (status writes, account switches, rebuild requests, host (re)creation) rather than letting concurrent callers race to read-modify-write; the latest writer should be made to wait for, not clobber, an in-flight write.

5. **Stamp published/async results with a revision/version** so a stale result can be refused by its consumer instead of silently overwriting newer state.

When reviewing async code, explicitly ask "what could change between this await and the next line?" and write a regression test that holds the await open (e.g. with a controllable promise) while the invalidating event happens, asserting the post-await code detects and handles the staleness instead of acting on outdated assumptions.