---
title: Guard async continuations against staleness
description: 'Most concurrency bugs in this codebase came from an async operation
  (a promise, a timer, a worker reply, a file read) completing after the state it
  was based on had already moved on: a component unmounted, a session was replaced,
  a set was refreshed, a file was rewritten, or a newer request superseded an older
  one. Treat every awaited continuation as...'
repository: cline/cline?ref=main
label: Concurrency
language: TypeScript
comments_count: 15
repository_stars: 70980
---

Most concurrency bugs in this codebase came from an async operation (a promise, a timer, a worker reply, a file read) completing after the state it was based on had already moved on: a component unmounted, a session was replaced, a set was refreshed, a file was rewritten, or a newer request superseded an older one. Treat every awaited continuation as potentially stale and defend against it explicitly:

1. **Capture an identity/generation token before the first await**, and re-check it immediately after each await before applying any effect (mutating shared state, resolving a caller's promise, writing to disk, touching a disposed resource). If the token no longer matches, drop the result silently (or route it through the current path) instead of acting on it.

```ts
const generation = ++this.generation;
const result = await doWork();
if (generation !== this.generation) return; // superseded; discard
this.apply(result);
```

2. **Claim shared, one-shot state synchronously, before any `await`**, not after. If a callback resolves a pending promise, takes a lock, or marks a resource "in use," do that claim on the first line of the handler. Otherwise a concurrent caller can observe the not-yet-claimed state during the gap and race in (e.g., two submissions both finding the same pending question still unresolved).

3. **Serialize competing writes to the same key** through a per-key promise queue (or an explicit lock) rather than letting independent async operations race to write last. A "last write wins" resolution order is only safe when writes are already chained; otherwise an earlier-started but slower write can silently overwrite a newer one.

4. **Revalidate identity immediately before a destructive action** instead of trusting an earlier check. For files, re-stat (inode/mtime/size) right before delete/overwrite with no intervening await; for in-memory resources, re-read the canonical map/registry right before disposing or swapping, and leave untouched anything that no longer matches.

5. **Stage replacements instead of mutating in place.** When replacing a live resource (a session, a cache entry, a connection), build and validate the replacement first, keep the original fully serving requests throughout, and only release/swap it in once the replacement is confirmed live. A failed replacement must leave the original intact and reachable.

Add a regression test for every such window: start the slow path, let a competing event or request arrive mid-flight, and assert the slow path's result is discarded (or correctly ordered) rather than corrupting state.