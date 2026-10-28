---
title: Safe locking under concurrency
description: When sharing state across threads, keep locks held only for short, non-blocking
  critical sections, and make lock-reacquisition and lock-ordering explicit rather
  than assumed.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70964
---

When sharing state across threads, keep locks held only for short, non-blocking critical sections, and make lock-reacquisition and lock-ordering explicit rather than assumed.

- Never perform a blocking operation (I/O, process spawn/wait, network/D-Bus calls) while holding a lock that other threads need for quick, time-sensitive work. If a blocking call is unavoidable, move it off the lock entirely: e.g. feed writes through an unbounded channel to a dedicated per-resource thread so the IPC/command thread only enqueues and returns immediately, instead of calling `write_all` under a mutex.
- Bound any blocking probe that runs on a latency-sensitive thread (main/UI thread) with an explicit timeout via a background thread + `recv_timeout`, and document which outcome the timeout resolves to and why (pick the cheaper failure mode, e.g. "stay hidden" vs. "quit and lose sessions").
- When a struct holds multiple locks, document the required acquisition order in a comment (e.g. "`process` may be held while acquiring `ws_endpoint`, never the reverse") and ensure every code path that needs both locks follows that order, including teardown/`stop()`/`Drop` paths.
- Re-check conditions that gate an action (e.g. "is this shutting down", "does this map still hold my entry") *after* acquiring the lock, not just before — an unlocked check-then-lock sequence is a TOCTOU race.
- When releasing a lock to do work and later mutating shared state based on the result, verify you're still acting on the same logical entity (via a generation counter, PID, or similar identity check) rather than just checking for presence, since the entry may have been replaced or removed in the meantime.

```rust
// Bad: blocking write_all held under the shared sessions lock.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(data.as_bytes())?;

// Good: hand the data to a dedicated writer thread via a channel; the
// command thread never blocks, and dropping the sender on session teardown
// ends the thread cleanly.
sender.send(data)?; // writer thread owns the real write_all call
```