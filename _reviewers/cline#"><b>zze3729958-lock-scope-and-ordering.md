---
title: Lock scope and ordering
description: 'Treat locks as protecting only in-memory state, never as a way to serialize
  blocking work. Keep critical sections minimal: acquire a lock only long enough to
  read/update shared state or to clone a handle, then release it before doing anything
  that can block (I/O, `write_all` on a pipe, spawning a process, waiting on a child,
  or probing an external service)....'
repository: cline/cline#"><b>zze3729958
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 71067
---

Treat locks as protecting only in-memory state, never as a way to serialize blocking work. Keep critical sections minimal: acquire a lock only long enough to read/update shared state or to clone a handle, then release it before doing anything that can block (I/O, `write_all` on a pipe, spawning a process, waiting on a child, or probing an external service). If an operation must block, move it onto its own dedicated thread fed by a channel rather than performing it under a mutex or on a synchronous command/UI-event thread — e.g. a PTY writer should own a per-session thread consuming from an `mpsc` channel so `terminal_write` only enqueues and returns immediately, instead of calling `write_all` while holding (or having just released) the sessions lock.

When more than one lock is involved, declare and enforce a single, documented acquisition order (e.g. "`process` may be held while acquiring `ws_endpoint`, never the reverse") so nested locking can't deadlock; anything that needs both must follow that order or take them strictly sequentially, never concurrently in two different orders.

Close check-then-act races by re-validating the invariant *under the lock*, immediately before mutating or acting on it — don't trust a check performed before the lock was taken (another thread may have changed state in between). Use this pattern for "start exactly once" logic (recheck shutdown/liveness under the process lock before spawning), and for install/replace logic (recheck the on-disk version/epoch under the installation lock immediately before overwriting the executable).

When a blocking call must run on a thread that cannot stall (GTK/UI main thread, IPC command thread), bound it explicitly: hand the work to a background thread and wait on it with a timeout via a channel, and make the timeout's fallback behavior the safe default (e.g. preserve existing behavior rather than risk data loss) rather than assuming the timeout always means "operation failed."

Finally, when state can be replaced or removed concurrently (e.g. a session map entry), don't let an async callback blindly remove/clear an entry by key — tag entries with a generation/identity and only mutate if the current entry still matches what the callback was started for, so a stale completion can't clobber a newer replacement.</description>
</invoke>
