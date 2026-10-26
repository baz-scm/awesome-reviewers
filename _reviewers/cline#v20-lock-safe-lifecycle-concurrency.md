---
title: Lock-Safe Lifecycle Concurrency
description: 'When using threads and shared state, treat three things as first-class:
  (1) lock scope, (2) lock order, and (3) ownership of background effects.


  **Standards**'
repository: cline/cline#v20
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70886
---

When using threads and shared state, treat three things as first-class: (1) lock scope, (2) lock order, and (3) ownership of background effects.

**Standards**
1. **Do not block while holding shared/global locks.**
   - Keep the shared lock only long enough to fetch/clone a per-resource handle, then release before any blocking operation (`write_all`, waits, long IPC, etc.).
   - If writes can block, route them through a per-resource worker (thread) and have the public API only enqueue work.

2. **Document and enforce lock ordering.**
   - If code ever needs more than one mutex, write an explicit lock-order rule (and enforce it everywhere). Never rely on “it seems to work”.

3. **Gate all background updates/cleanup by ownership identity.**
   - Background threads may outlive the state they started with (e.g., a session replaced in a map, a child process swapped). Require an identity check (generation token or child pid) before removing entries or mutating shared fields.

4. **Move slow/probe/IO work off main/UI threads with time bounds.**
   - If a call might hang or take significant time, run it on a worker thread and use a timeout in the caller; an overrun worker may finish independently.

**Practical patterns**
- *Short-lock handle capture (instead of blocking under the lock)*:
  ```rust
  let writer = {
      let mut sessions = state.sessions.lock().unwrap();
      sessions.get_mut(&id)
          .ok_or("missing")?
          .writer
          .clone_handle() // or clone a per-session writer/guard
  }; // drop sessions lock here

  // Now safe to do potentially blocking IO
  writer.write_all(data.as_bytes())?;
  ```

- *Per-session writer worker (enqueue only)*:
  ```rust
  // terminal_write: lock-free enqueue
  tx.send(data).map_err(|_| "writer stopped")?;
  // writer thread owns the blocking write_all
  ```

- *Ownership-gated cleanup (generation/child pid)*:
  ```rust
  // in reader/cleanup thread
  if map.get(&id).is_some_and(|s| s.generation == my_generation) {
      map.remove(&id);
  }
  ```

**Why**
These rules prevent deadlocks and UI stalls, and eliminate “stale thread clobbered newer state” race bugs that commonly appear in multi-session, child-process, and map-backed concurrency designs.