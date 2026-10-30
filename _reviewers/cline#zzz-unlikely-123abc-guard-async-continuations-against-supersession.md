---
title: Guard async continuations against supersession
description: Across the codebase, the single most common concurrency bug is an async
  operation (a fetch, handshake, planner call, session rebuild, status read, or reconnect)
  whose continuation runs after it has been superseded — by a newer request for the
  same resource, a reconnect, a teardown, an account/scope change, or a replacement
  session — and clobbers state that...
repository: cline/cline#zzz-unlikely-123abc
label: Concurrency
language: TypeScript
comments_count: 26
repository_stars: 71035
---

Across the codebase, the single most common concurrency bug is an async operation (a fetch, handshake, planner call, session rebuild, status read, or reconnect) whose continuation runs after it has been superseded — by a newer request for the same resource, a reconnect, a teardown, an account/scope change, or a replacement session — and clobbers state that no longer belongs to it. This happens because the check for "is this still relevant?" is done once before the `await`, not again when it resumes.

Whenever a function awaits something and then mutates shared state, dispatches a result, or starts another side effect, it must re-validate that it is still the current owner of that state immediately before acting, with no further await in between the check and the mutation. Use a cheap, monotonically increasing fencing token (a "generation"/"epoch"/bind id/run id) that is bumped synchronously whenever the owning context changes (new bind, new scope, new start, cancel, teardown), and capture that token before the first await. On resume, compare the captured token to the current one; if they differ, drop the result instead of applying it. For resources that must stay open until a caller currently needs them, use a pin/reference count instead of a boolean, so concurrent users of the same resource don't tear it down from under each other. When multiple writers can race to mutate the same state, prefer chaining each operation onto the previous one via a shared promise (an explicit mutex/queue) over ad-hoc flags, so operations serialize and each one observes the outcome of the one before it.

Example pattern:
```ts
async function bindAndFetch(id: string) {
  generation += 1;
  const myGeneration = generation; // capture before any await
  boundId = id;
  const result = await fetchStateFor(id);
  if (myGeneration !== generation) return; // superseded while awaiting; drop it
  applyState(result);
}

function unbind() {
  generation += 1; // invalidates any in-flight bind's continuation
  boundId = "";
}
```

Apply this check at every point where an async result is about to be dispatched, written to a store, used to decide whether to detach/dispose a connection, or used to resolve a pending caller — not just at the start of the function. Prefer dropping stale work silently over letting it "win" a race with fresher work, and when a resource is still in use by another in-flight operation, pin it rather than disposing it just because its current owner looks idle.