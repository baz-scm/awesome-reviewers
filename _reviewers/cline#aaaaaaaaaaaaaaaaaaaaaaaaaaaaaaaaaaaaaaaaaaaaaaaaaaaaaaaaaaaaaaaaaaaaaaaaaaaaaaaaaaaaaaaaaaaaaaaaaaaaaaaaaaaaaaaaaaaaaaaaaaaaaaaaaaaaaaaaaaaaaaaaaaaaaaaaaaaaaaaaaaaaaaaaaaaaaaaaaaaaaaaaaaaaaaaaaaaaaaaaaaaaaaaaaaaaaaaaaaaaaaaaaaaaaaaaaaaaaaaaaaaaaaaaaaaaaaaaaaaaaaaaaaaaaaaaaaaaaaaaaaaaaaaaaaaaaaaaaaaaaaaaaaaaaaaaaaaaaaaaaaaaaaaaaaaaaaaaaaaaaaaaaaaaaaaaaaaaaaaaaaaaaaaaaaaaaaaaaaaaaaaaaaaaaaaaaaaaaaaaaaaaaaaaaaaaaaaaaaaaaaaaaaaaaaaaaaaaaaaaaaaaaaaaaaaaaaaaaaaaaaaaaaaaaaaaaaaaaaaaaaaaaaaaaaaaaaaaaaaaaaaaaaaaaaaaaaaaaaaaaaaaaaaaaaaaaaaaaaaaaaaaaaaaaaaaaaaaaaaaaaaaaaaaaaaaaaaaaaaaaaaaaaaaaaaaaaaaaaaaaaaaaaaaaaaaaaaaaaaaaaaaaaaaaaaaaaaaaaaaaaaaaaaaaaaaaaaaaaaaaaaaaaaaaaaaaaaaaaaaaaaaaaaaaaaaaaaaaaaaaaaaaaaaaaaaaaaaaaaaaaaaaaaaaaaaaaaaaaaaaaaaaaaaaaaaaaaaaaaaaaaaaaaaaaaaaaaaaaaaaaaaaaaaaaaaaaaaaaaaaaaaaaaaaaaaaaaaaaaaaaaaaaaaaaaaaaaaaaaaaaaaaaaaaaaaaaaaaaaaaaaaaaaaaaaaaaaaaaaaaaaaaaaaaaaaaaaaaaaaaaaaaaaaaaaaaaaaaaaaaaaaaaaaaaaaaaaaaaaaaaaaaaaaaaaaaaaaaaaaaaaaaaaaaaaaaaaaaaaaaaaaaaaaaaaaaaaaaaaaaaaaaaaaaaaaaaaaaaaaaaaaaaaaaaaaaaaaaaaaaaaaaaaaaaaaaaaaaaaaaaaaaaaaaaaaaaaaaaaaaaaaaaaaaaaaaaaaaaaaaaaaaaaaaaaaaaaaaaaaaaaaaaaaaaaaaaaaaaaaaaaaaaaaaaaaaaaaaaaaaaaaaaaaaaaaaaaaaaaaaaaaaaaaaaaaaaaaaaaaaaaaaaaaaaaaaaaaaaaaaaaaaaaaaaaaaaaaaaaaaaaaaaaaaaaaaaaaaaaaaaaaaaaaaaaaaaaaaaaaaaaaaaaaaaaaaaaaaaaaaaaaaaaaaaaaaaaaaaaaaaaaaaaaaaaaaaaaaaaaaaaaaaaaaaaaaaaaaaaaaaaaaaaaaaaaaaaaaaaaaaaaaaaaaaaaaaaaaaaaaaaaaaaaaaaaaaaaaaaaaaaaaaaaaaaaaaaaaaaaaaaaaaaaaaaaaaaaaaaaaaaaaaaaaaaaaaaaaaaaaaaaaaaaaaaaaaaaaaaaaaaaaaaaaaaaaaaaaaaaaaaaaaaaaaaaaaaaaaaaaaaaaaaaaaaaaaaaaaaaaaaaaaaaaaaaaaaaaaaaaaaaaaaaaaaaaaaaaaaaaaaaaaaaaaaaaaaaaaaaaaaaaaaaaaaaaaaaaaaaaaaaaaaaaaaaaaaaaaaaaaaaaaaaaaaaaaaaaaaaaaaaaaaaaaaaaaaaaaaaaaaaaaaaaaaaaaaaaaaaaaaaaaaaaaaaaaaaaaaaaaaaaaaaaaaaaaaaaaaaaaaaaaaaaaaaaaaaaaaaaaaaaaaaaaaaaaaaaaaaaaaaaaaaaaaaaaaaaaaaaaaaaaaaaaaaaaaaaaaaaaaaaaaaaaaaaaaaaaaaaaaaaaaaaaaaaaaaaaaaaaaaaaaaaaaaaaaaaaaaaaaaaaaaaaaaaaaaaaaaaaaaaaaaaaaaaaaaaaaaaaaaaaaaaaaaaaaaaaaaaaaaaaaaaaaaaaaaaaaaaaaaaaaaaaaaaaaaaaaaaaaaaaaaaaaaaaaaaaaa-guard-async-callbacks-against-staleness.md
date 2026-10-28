---
title: Guard async callbacks against staleness
description: 'Most of the concurrency bugs found in review share one shape: code awaits
  something (a network call, a worker reply, a rebuild, a spawn) and then mutates
  shared state or acts on the result, but by the time the await resolves, the world
  has moved on — a newer request was made, the target was torn down, a session/tab/bind
  was replaced, or another caller...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TypeScript
comments_count: 22
repository_stars: 70968
---

Most of the concurrency bugs found in review share one shape: code awaits something (a network call, a worker reply, a rebuild, a spawn) and then mutates shared state or acts on the result, but by the time the await resolves, the world has moved on — a newer request was made, the target was torn down, a session/tab/bind was replaced, or another caller already claimed the operation. The fix is always the same pattern:

1. Before starting an async operation that will later mutate shared state, record (or bump) a generation/version/epoch token, or capture an identity reference (e.g. the current session object, bound id, worker instance).
2. When the async operation resolves, re-check that the token/identity is still current before applying the effect. If it isn't, discard the result (or, for cleanup paths, retarget it) instead of writing stale data over newer state.
3. For "claim once" operations (resolving a pending question, starting a generation, taking a lease), make the claim synchronously, before the first await, so a second concurrent caller cannot slip into the same window and double-handle the same event.
4. For teardown/release paths, gate the actual deletion/dispose on "this resource still occupies its slot" (identity comparison), not merely on "we started releasing it," so a resource that was already replaced during the awaited work is never evicted out from under its replacement.

Apply this whenever you see: a retry/reconnect that could resolve after a newer attempt already succeeded, a bind/attach/detach pair where detach can race the in-flight attach's reply, a cache or state store written from a background refresh, or a resident object replaced via "rebuild in place."

```ts
class Example {
  private generation = 0;
  private current?: Session;

  async rebuild(next: Config): Promise<void> {
    const generation = ++this.generation; // bump before awaiting
    const built = await buildSession(next);
    if (generation !== this.generation) {
      // superseded while we were building; discard, don't install
      await built.dispose();
      return;
    }
    const old = this.current;
    this.current = built;
    // release the old one only if it's still the one we replaced
    if (old && this.current !== old) await old.dispose();
  }
}
```

Write a regression test that holds the async step open while a second, superseding operation runs to completion, and assert the first operation's late result is discarded rather than applied.