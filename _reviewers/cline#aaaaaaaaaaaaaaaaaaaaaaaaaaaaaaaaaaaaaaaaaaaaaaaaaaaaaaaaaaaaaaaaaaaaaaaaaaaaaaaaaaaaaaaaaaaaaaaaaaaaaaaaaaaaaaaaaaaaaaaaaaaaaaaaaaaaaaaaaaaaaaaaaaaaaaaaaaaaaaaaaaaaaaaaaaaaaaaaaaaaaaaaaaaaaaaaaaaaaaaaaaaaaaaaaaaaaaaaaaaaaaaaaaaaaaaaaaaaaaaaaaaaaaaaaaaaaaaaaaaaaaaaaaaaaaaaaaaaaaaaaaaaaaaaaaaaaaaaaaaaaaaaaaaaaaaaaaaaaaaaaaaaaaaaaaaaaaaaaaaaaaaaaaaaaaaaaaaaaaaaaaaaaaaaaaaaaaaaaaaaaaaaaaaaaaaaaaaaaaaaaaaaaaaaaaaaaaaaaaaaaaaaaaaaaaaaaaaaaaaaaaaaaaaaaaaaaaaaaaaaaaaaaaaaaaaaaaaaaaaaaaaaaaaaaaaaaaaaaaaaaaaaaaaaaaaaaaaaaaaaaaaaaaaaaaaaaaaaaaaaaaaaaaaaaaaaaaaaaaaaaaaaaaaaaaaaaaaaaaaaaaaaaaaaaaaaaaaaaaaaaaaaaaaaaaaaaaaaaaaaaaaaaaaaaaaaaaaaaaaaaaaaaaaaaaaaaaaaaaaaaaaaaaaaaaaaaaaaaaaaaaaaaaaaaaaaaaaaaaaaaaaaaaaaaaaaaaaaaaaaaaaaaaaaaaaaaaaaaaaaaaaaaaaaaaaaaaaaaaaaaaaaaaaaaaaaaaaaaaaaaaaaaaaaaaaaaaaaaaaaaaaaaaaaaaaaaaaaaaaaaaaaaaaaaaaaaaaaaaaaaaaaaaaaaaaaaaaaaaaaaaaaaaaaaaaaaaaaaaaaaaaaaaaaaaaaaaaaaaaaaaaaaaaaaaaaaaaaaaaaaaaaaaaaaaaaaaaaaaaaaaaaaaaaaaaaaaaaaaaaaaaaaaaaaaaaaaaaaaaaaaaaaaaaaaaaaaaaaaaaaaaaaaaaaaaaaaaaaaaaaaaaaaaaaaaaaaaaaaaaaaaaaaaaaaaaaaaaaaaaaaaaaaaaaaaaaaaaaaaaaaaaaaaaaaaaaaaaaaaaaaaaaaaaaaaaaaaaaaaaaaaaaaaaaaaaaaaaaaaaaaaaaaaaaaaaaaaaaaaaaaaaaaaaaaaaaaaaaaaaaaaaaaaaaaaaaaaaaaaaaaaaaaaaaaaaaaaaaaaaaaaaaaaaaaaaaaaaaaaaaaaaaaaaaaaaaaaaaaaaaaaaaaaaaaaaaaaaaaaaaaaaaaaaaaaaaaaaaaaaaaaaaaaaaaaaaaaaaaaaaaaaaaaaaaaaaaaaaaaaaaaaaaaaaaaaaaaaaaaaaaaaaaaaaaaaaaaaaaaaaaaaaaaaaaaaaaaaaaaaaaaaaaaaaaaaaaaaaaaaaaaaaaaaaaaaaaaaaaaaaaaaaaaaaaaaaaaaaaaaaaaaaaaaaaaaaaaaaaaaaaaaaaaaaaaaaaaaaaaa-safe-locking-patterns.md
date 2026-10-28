---
title: Safe locking patterns
description: When sharing mutable state across threads, keep critical sections small
  and free of blocking work, and treat any check made before acquiring a lock as stale.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70965
---

When sharing mutable state across threads, keep critical sections small and free of blocking work, and treat any check made before acquiring a lock as stale.

1. Never hold a lock while performing a blocking operation (I/O, process wait, syscalls). A blocked call inside a lock stalls every other thread waiting on it, including the sync command thread serving IPC/UI requests. Instead, clone/queue what's needed, release the lock, then do the blocking work off that lock — or move the blocking work to a dedicated thread fed by a channel:
```rust
// Bad: write_all runs while holding the shared sessions lock.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id)?.writer.write_all(data.as_bytes())?;

// Good: enqueue onto a per-session writer thread; the lock only
// protects the handle lookup, never the blocking write.
let tx = {
    let sessions = state.sessions.lock().unwrap();
    sessions.get(&id)?.write_tx.clone()
};
tx.send(data).ok(); // writer thread owns the actual write_all
```

2. Treat any state checked before taking a lock (e.g. "is this installed version stale?", "is the app shutting down?") as potentially outdated by the time the lock is acquired. Re-validate the condition under the lock, immediately before the mutation it gates, rather than trusting an earlier unlocked read — this closes check-then-act (TOCTOU) races between concurrent callers.

3. When a flow needs more than one lock (e.g. a process handle and an endpoint value), define and document a single, fixed acquisition order and enforce it everywhere that flow touches both locks, including teardown paths. This prevents deadlocks from two code paths acquiring the same pair of locks in opposite order.

4. When multiple async producers can update the same shared slot (replaced child process, replaced session, retried spawn), tag the authoritative value with a generation id or stable identity (pid, session generation) and verify that identity still matches under the lock before clearing or overwriting it. This stops a late callback from a superseded operation from clobbering state already set by its successor.

5. For operations that must not block if already in progress (manual retry triggers, idempotent cleanup), prefer `try_lock` over `lock` so a concurrent call is a no-op rather than a stall.

Apply this discipline any time a design introduces a `Mutex`/channel pair guarding process lifecycle, I/O streams, or installed/shared resources.