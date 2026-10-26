---
title: Avoid Blocking While Locked
description: 'When adding or modifying concurrency, follow these rules to prevent
  deadlocks, UI stalls, and racey shutdowns:


  1) Keep lock hold-time minimal

  - Only hold a shared/global lock (e.g., a sessions HashMap) to look up/replace state.'
repository: Cline/Cline
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70840
---

When adding or modifying concurrency, follow these rules to prevent deadlocks, UI stalls, and racey shutdowns:

1) Keep lock hold-time minimal
- Only hold a shared/global lock (e.g., a sessions HashMap) to look up/replace state.
- Release the lock before any potentially blocking operation (I/O, thread joins, channel sends that could block, etc.).

2) Isolate blocking work in dedicated workers
- For long-running/blocking I/O, create a per-entity worker thread.
- Expose a fast, non-blocking API by sending work over an mpsc channel (enqueue), rather than performing the blocking call on the caller’s thread.

3) Make teardown race-safe
- Threads often outlive state they were spawned with.
- When removing/replacing sessions, ensure a stale worker can’t remove the wrong entry (e.g., generation/tag checks).
- Ensure workers terminate deterministically (e.g., dropping the sender end so the worker loop exits; or killing the underlying process/closing the PTY).

4) Never stall critical threads; use offload + timeouts
- If a function can block (D-Bus, IPC, filesystem/network, etc.) and is called from a UI/close-handler path, run it on a worker thread and use a timeout.
- Document the timeout’s resolution policy so behavior is stable and intentional.

Illustrative pattern (lock scope + per-session worker):

```rust
// Shared map lock only for short lookup/handle cloning.
let writer_tx = {
    let mut sessions = state.sessions.lock().unwrap_or_else(|e| e.into_inner());
    let session = sessions.get_mut(&id).ok_or("missing session")?;
    session.writer_tx.clone() // clone/enqueue handle; do not keep the lock
};

// Fast, non-blocking enqueue; actual blocking happens in the worker.
writer_tx.send(data).map_err(|_| "writer stopped")?;

// Worker thread owns the blocking write.
thread::spawn(move || {
    while let Ok(chunk) = rx.recv() {
        // blocking write_all happens here, not on the caller/UI thread
        let _ = session_writer.write_all(&chunk);
    }
});
```

Apply these rules whenever you touch: locks protecting shared state, IPC/UI entrypoints, PTY/stdin/stdout plumbing, shutdown/replace logic, or any potentially slow probe.