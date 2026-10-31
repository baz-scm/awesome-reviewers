---
title: Avoid blocking while holding locks
description: Keep critical sections short and never perform a blocking operation (I/O,
  process spawn/wait, inter-thread RPC) while a lock is held, since a stalled call
  blocks every other thread waiting on that mutex — including the synchronous command/IPC
  thread. Shrink lock scope to just the data access, clone or move what's needed out
  of the guard, and release the...
repository: cline/cline?foo=bar
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 71082
---

Keep critical sections short and never perform a blocking operation (I/O, process spawn/wait, inter-thread RPC) while a lock is held, since a stalled call blocks every other thread waiting on that mutex — including the synchronous command/IPC thread. Shrink lock scope to just the data access, clone or move what's needed out of the guard, and release the lock before doing anything that can block.

When an operation is inherently blocking (e.g. writing to a PTY, spawning/killing a process, waiting on a child), move it off the lock-holding thread entirely: dedicate a worker thread per resource and communicate via an mpsc channel, so callers only enqueue work instead of blocking. For example, instead of locking a session map and calling a blocking `write_all` inline, give each session its own writer thread fed by a channel:

```rust
// Caller just enqueues; it never blocks on the shell.
fn terminal_write(id: &str, data: Vec<u8>) {
    let sender = sessions.lock().unwrap().get(id).map(|s| s.writer_tx.clone());
    if let Some(tx) = sender {
        let _ = tx.send(data); // writer thread owns the blocking write_all
    }
}
```

If multiple locks must be held together, document and enforce a single, fixed acquisition order (e.g. "lock A before B, never B before A") so nested lock paths can't deadlock, and make `stop`/shutdown code follow the same order as the hot path.

When state can legitimately be replaced or raced (a session reinserted under the same key, a child process exiting while a reader thread is draining it), identify the specific instance you're updating — a generation counter or PID check taken under the lock — rather than trusting a bare key lookup, so a stale background thread can't clobber a newer entry.

For time-bounded cross-thread checks (a probe run on another thread with `recv_timeout`), decide and document which outcome a timeout should resolve to, favoring the cheaper, more recoverable mistake, and write a test that pins that behavior (e.g. a slow-but-present responder should not be treated the same as "absent").