---
title: Avoid Lock-Blocking I/O
description: 'Rule: Don’t do potentially blocking work while holding a shared lock
  or while on a critical thread. Instead, narrow lock scope to quick state access,
  and move I/O to per-resource workers.'
repository: cline/cline#v28
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70893
---

Rule: Don’t do potentially blocking work while holding a shared lock or while on a critical thread. Instead, narrow lock scope to quick state access, and move I/O to per-resource workers.

Apply:
- Lock scope: If you must access shared session state, lock only to clone/get a handle, then release before any blocking call (e.g., `write_all`, socket reads, PTY operations).
- Decouple I/O: For each session/resource, use a dedicated worker (thread/task) plus a queue (e.g., `mpsc`) so commands just enqueue.
- Safe lifecycle/race cleanup: When removing state from a shared map in a worker, ensure it still owns the same “generation”/identity so stale workers can’t delete newer sessions.
- Timeouts on critical threads: Run probes on a separate thread/task and enforce a bounded wait; document which error direction is acceptable.

Sketch (pattern):
```rust
// shared map: only holds lightweight handles/state
let writer_tx = {
    let mut map = sessions.lock()?;
    map.get_mut(&id).ok_or("missing")?.writer_tx.clone()
};
// lock released before blocking/IO
writer_tx.send(data).map_err(|_| "writer stopped")?;

// per-session worker
std::thread::spawn(move || {
    while let Ok(chunk) = rx.recv() {
        // blocking write happens here, not under shared locks
        let _ = writer.write_all(&chunk);
    }
    // exiting worker ends when sender is dropped
});

// stale cleanup guard (conceptual)
if map.get(&id).map(|s| s.generation) == Some(my_generation) {
    map.remove(&id);
}
```

If you need a timeout-based decision, do the probe off the critical thread:
- spawn the probe,
- `recv_timeout(timeout)` on the caller,
- document the intentional tradeoff for which “wrong” outcome is cheaper.