---
title: Avoid Blocking Under Locks
description: When implementing concurrent/background work, design so that (1) shared
  locks are held for short, non-blocking critical sections, (2) blocking I/O is handled
  outside the lock and often outside the request/UI thread, and (3) background tasks
  cannot corrupt state after ownership/lifecycle changes.
repository: cline/cline#v29
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70893
---

When implementing concurrent/background work, design so that (1) shared locks are held for short, non-blocking critical sections, (2) blocking I/O is handled outside the lock and often outside the request/UI thread, and (3) background tasks cannot corrupt state after ownership/lifecycle changes.

Apply:
- Minimize lock scope: take what you need (e.g., clone a handle) and release the lock before any `write_all`, `read`, waits, or IPC sends that may block.
- Isolate blocking I/O with an owner worker:
  - Use a per-session (or per-resource) worker thread that owns the blocking writer.
  - Let request handlers only enqueue work via a channel.
  - Stop the worker by dropping the sender/owner, so shutdown is deterministic.
- Make cleanup/race conditions explicit:
  - Use generation/epoch/ownership tokens so a reader thread only removes/updates shared state if it still matches the current generation.

Sketch:
```rust
// Shared map holds per-session state; request takes lock briefly.
let writer = {
    let mut map = sessions.lock().unwrap();
    map.get_mut(&id).ok_or("missing")?.writer_handle_cloned()
}; // lock released here

// Enqueue instead of blocking in the caller.
writer_tx.send(data).map_err(|_| "session ended")?;

// Worker owns the blocking write.
std::thread::spawn(move || {
    while let Ok(chunk) = rx.recv() {
        let _ = blocking_writer.write_all(&chunk);
    }
});

// Cleanup guarded by generation.
if map.get(&id).is_some_and(|s| s.generation == my_generation) {
    map.remove(&id);
}
```

Also: if you use timeouts to probe external state from a critical thread (UI/close handlers), enforce a strict timeout and document the asymmetric “wrong answer” direction so the failure mode is safe.