---
title: Guard shared mutable state
description: 'When multiple threads can read, replace, or tear down shared state concurrently,
  protect it with more than a bare mutex:


  1. Never block while holding a lock. A lock should only guard a brief read/write
  of state, never a blocking I/O call, a process wait, or a channel send that can
  stall. If an operation can block (writing to a pipe, waiting on a child...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70970
---

When multiple threads can read, replace, or tear down shared state concurrently, protect it with more than a bare mutex:

1. Never block while holding a lock. A lock should only guard a brief read/write of state, never a blocking I/O call, a process wait, or a channel send that can stall. If an operation can block (writing to a pipe, waiting on a child process, a blocking IPC call), take the lock only to clone/extract what you need, release it, then block. For work that must be serialized but can legitimately block for a long time (e.g. feeding a PTY writer), hand it off to a dedicated worker thread fed by a channel instead of doing it under the lock on the calling thread.

2. Tag replaceable resources with an identity or generation so a stale background thread can't clobber its successor's state. When a resource (a session, a child process, a cache entry) can be replaced while an old reader/writer/waiter thread for it is still running, that thread must verify it still "owns" the current entry before mutating shared state:

```rust
// Each spawn gets a fresh generation; a thread tied to an old instance
// must not evict or overwrite the current one.
let generation = NEXT_GENERATION.fetch_add(1, Ordering::Relaxed);
sessions.lock().unwrap().insert(id.clone(), Session { generation, .. });

// In the background thread, on completion:
let mut map = sessions.lock().unwrap();
if map.get(&id).is_some_and(|s| s.generation == generation) {
    map.remove(&id); // safe: still the same instance
}
```
The same applies to tracking a child process by `pid`/`Child::id()` before clearing shared endpoint/state on exit.

3. Close check-then-act gaps by re-validating the condition under the lock immediately before the mutating action, especially for install/replace/upgrade flows (e.g., re-checking a build epoch while holding the installation lock right before swapping an executable). Don't trust a check performed before the lock was acquired.

4. When more than one lock must be held together, document and enforce a single, fixed acquisition order (e.g., "lock A may be held while acquiring lock B, never the reverse") so no code path can deadlock by nesting locks in the opposite order.

5. Prefer relying on documented, idempotent OS/runtime semantics (e.g., `Child::kill`/`wait` returning `Ok` for an already-reaped process) over adding extra bookkeeping to special-case already-finished work, but verify that behavior for your target platforms before depending on it.

Applying these consistently prevents the class of bugs where a blocked writer stalls the whole IPC thread, a late reader thread deletes a session that was already replaced, or a race between a health check and a respawn spawns duplicate processes.