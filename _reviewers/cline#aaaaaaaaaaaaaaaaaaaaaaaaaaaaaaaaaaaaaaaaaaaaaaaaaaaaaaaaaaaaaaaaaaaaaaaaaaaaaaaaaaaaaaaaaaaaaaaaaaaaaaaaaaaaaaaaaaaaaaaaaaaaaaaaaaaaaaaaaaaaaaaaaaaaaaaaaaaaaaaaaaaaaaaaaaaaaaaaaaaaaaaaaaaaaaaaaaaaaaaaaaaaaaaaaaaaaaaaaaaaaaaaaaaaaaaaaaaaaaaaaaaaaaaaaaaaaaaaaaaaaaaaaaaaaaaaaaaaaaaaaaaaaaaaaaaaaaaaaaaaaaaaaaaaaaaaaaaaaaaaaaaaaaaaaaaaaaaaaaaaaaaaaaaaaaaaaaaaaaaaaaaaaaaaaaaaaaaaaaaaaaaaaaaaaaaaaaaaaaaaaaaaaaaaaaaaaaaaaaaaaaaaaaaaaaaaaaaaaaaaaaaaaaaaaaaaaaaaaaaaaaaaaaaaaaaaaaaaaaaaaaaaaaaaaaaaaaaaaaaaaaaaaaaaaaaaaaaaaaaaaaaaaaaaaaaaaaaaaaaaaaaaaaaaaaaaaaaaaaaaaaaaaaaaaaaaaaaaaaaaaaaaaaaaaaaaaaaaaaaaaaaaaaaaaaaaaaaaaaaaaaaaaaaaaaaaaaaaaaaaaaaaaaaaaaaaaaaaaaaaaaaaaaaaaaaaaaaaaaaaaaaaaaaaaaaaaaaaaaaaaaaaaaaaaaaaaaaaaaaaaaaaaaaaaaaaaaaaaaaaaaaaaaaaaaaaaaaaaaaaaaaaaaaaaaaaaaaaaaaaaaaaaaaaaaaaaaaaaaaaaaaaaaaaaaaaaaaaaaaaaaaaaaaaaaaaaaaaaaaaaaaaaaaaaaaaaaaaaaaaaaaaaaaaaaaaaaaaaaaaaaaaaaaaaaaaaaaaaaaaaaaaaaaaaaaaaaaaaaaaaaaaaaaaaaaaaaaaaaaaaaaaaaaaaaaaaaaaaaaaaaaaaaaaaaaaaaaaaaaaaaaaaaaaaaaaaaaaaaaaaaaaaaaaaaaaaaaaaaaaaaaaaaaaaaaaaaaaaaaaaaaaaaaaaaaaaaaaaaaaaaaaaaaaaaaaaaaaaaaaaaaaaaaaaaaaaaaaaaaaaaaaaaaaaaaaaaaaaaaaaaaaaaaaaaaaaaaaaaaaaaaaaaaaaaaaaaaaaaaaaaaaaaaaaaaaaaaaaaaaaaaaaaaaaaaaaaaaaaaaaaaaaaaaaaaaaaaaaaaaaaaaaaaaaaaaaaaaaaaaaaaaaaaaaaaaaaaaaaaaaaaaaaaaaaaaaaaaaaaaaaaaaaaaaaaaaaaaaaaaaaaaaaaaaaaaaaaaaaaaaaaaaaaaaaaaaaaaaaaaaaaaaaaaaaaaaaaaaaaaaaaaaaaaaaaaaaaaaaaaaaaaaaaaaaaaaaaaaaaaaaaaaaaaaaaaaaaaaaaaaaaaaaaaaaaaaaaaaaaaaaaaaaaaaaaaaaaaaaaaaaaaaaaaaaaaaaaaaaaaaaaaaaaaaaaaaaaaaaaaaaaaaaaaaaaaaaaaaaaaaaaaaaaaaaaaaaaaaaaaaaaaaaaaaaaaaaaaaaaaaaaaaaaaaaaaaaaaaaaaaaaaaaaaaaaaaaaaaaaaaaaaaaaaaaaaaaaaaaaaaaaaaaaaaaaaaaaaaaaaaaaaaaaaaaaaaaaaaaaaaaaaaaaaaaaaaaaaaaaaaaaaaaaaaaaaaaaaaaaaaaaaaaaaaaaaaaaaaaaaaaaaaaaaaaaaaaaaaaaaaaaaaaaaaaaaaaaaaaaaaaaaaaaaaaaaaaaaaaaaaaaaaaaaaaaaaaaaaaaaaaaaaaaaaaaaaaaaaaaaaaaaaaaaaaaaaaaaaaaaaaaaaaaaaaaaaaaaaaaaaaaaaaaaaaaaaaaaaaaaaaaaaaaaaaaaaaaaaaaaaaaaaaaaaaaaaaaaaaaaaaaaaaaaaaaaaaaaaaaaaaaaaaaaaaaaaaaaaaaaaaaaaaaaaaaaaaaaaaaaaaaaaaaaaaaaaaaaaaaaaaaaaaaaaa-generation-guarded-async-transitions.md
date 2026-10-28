---
title: Generation-guarded async transitions
description: Most concurrency bugs found in review came from async operations that
  span multiple `await`s while the state they depend on (a session, a connection,
  an account scope, a cached entry) can be replaced, reset, or torn down concurrently.
  A stale callback then applies its result on top of newer state, double-runs cleanup,
  or races another caller for the same...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TypeScript
comments_count: 14
repository_stars: 70967
---

Most concurrency bugs found in review came from async operations that span multiple `await`s while the state they depend on (a session, a connection, an account scope, a cached entry) can be replaced, reset, or torn down concurrently. A stale callback then applies its result on top of newer state, double-runs cleanup, or races another caller for the same write. Apply these two complementary rules to any multi-step async operation on shared, replaceable state:

1. **Tag the state with a generation/epoch, and re-check it after every await.** Capture the current generation (or object identity) before starting async work; after each `await`, compare it to the live value before applying results, writing data, or touching listeners. Discard the result silently if the generation moved on. This closes the whole class of "stale reply overwrites fresher state," "detach fired before an in-flight attach's reply landed," and "the diff baseline is the latest list, not the one this session was built from" bugs.

```ts
const generation = ++this.generation;
const result = await doAsyncWork();
if (generation !== this.generation) return; // superseded; drop it
this.apply(result);
```

2. **When replacing a resource, build/register the replacement before tearing down the old one, and release the old one only by identity.** Never free, stop, or delete a slot just because "a replacement was requested" — gate teardown on the slot still pointing at the object you started with (`if (this.sessions.get(id) === oldResident) release(oldResident)`), and run that release in a `finally` so it happens whether the rebuild succeeded or failed. This avoids both stranding the old resource and destroying a live replacement that already won the race.

For operations that must not interleave at all (writing the same file/record, switching an account, replacing a cached host), don't rely on generation checks alone — serialize them through a per-key promise chain so each request runs only after the previous one settles and decides against the state as it is then:

```ts
private pending = Promise.resolve();
run(op: () => Promise<void>): Promise<void> {
  const next = this.pending.then(op, op); // run after prior settles, even on rejection
  this.pending = next;
  return next;
}
```

When a trigger can be claimed by more than one concurrent caller (resolving a pending question, pinning a host someone else is also resolving), claim or mark ownership synchronously, before the first `await`, so a second caller sees the claim and defers rather than racing to the same answer. Add a regression test that holds one operation mid-flight while a second, newer request arrives, and assert the newer one wins and the stale one is a no-op.