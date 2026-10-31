---
title: Guard against stale async writes
description: Many bugs in this codebase came from an async operation (a read, a connect,
  a status write, a rebuild, a refresh) completing after a newer operation had already
  changed the state it was about to write to. Because the second writer "won" only
  by finishing first rather than by being the most recent, the result was lost updates,
  resurrected stale data, or...
repository: cline/cline?foo=bar
label: Concurrency
language: TypeScript
comments_count: 16
repository_stars: 71082
---

Many bugs in this codebase came from an async operation (a read, a connect, a status write, a rebuild, a refresh) completing after a newer operation had already changed the state it was about to write to. Because the second writer "won" only by finishing first rather than by being the most recent, the result was lost updates, resurrected stale data, or state applied to the wrong session/epoch/generation (e.g. `GitHubConnector.refresh` overwriting the live snapshot with its own stale one, a session-status write landing after teardown's `cancelled`, a plugin UI epoch emitting before a newer one was promoted, a rebuild replacing a resident session before the replacement was confirmed live, two reads of "live" vs "persisted" transcript racing each other).

To avoid this class of bug:
1. **Tag every async operation with an identity/generation/epoch captured before the first await**, and re-check it immediately before any mutation of shared state: `if (generation !== this.currentGeneration) return;`. Do this at every point the operation resumes after an `await`, not just once at the end.
2. **Apply results as patches onto the live/current state, not as wholesale replacements built from a stale snapshot.** When concurrent operations touch the same key (a file path, a session id, a cache entry), merge into the current value rather than overwrite it.
3. **Serialize writes to a single shared resource** (status fields, files, account scope) through a per-key promise chain or lock, so a slow write cannot land after a later one; don't rely on whichever write merely resolves last.
4. **When replacing a resource (a session runtime, a cache entry, a connection), build and install the replacement first, then release the old one guarded by identity** (`if (this.map.get(key) === oldValue) this.map.delete(key)`), so a slow teardown of the old resource can never evict a newer resident.
5. Add a regression test that deliberately holds the slower operation open while a newer one completes, and asserts the newer state survives.

Example shape:
```ts
const generation = this.generation;
const result = await slowOperation();
if (generation !== this.generation || this.disposed) return; // stale: drop it
this.state = mergeIntoCurrent(this.state, result);
```