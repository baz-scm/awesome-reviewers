---
title: Safe locking and threading
description: Shared mutable state accessed from multiple threads (IPC command handlers,
  UI/main-loop threads, background workers) must be protected with locks that are
  held for the shortest time possible and never across a blocking operation. A blocking
  write, wait, or external probe (process I/O, D-Bus call, child.wait()) performed
  while holding a lock, or run directly...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70986
---

Shared mutable state accessed from multiple threads (IPC command handlers, UI/main-loop threads, background workers) must be protected with locks that are held for the shortest time possible and never across a blocking operation. A blocking write, wait, or external probe (process I/O, D-Bus call, child.wait()) performed while holding a lock, or run directly on a thread other components depend on (the sync IPC thread, the GTK main thread), will stall every other caller of that lock/thread. Instead, hand the blocking work off to a dedicated worker thread fed by a channel, and only use the lock to enqueue work or swap a cheap handle:

```rust
// Bad: write_all under the sessions lock blocks the IPC command thread.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(&data)?;

// Good: enqueue onto a per-session writer thread; the lock is only
// touched to look up the sender.
let input = {
    let sessions = state.sessions.lock().unwrap();
    sessions.get(&id).unwrap().input.clone()
};
input.send(data).ok();
```

When an operation must be bounded (probing an external service, waiting on a shell), run it on a separate thread and join it via `recv_timeout`/similar rather than blocking the caller indefinitely, and pick a conservative, documented fallback for the timeout case.

If more than one lock can be live at the same time, define and document a single acquisition order (e.g. "`process` may be held while acquiring `ws_endpoint`, never the reverse") and make every caller that needs both locks follow it, to avoid deadlocks.

Finally, protect against races created by concurrent state replacement or shutdown: tag long-lived resources with a monotonic generation/id so a stale thread (an old reader, a queued respawn) cannot act on a resource that has since been replaced, and re-check atomic flags (e.g. a `shutting_down` flag) after acquiring the lock, not just before, since the unlocked check can go stale between the check and the lock acquisition.