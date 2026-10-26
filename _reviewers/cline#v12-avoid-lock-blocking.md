---
title: Avoid lock blocking
description: 'When concurrency involves blocking I/O or cross-thread IPC, keep critical
  threads responsive and prevent lock contention.


  Apply this standard:

  - Don’t hold shared/global locks while performing `write_all`, network/PTY reads,
  or any potentially-blocking call. Copy/clone the minimum handle under the lock,
  then release it before blocking.'
repository: cline/cline#v12
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70872
---

When concurrency involves blocking I/O or cross-thread IPC, keep critical threads responsive and prevent lock contention.

Apply this standard:
- Don’t hold shared/global locks while performing `write_all`, network/PTY reads, or any potentially-blocking call. Copy/clone the minimum handle under the lock, then release it before blocking.
- Offload blocking work from request/command/GUI threads into per-resource worker threads (or an async task) and communicate via channels.
- Use bounded waits on the caller side (timeouts) for probes or remote calls; if a probe exceeds the timeout, let it finish without blocking the critical path.
- Make lifecycle/race behavior explicit: when a session can be replaced or removed asynchronously, ensure the worker removes state only if it still owns the expected session (e.g., generation/id checks), and ensure shutdown drops senders / closes PTYs so blocked operations can unwind.

Example pattern (lock-scope + worker thread):
```rust
// BAD: don't do blocking I/O under a global mutex.
// GOOD: clone handle under lock, then release before blocking.
let writer = {
    let mut sessions = state.sessions.lock()?;
    sessions.get_mut(&id).map(|s| s.writer.clone_handle())?
};
writer.write_all(data.as_bytes())?;

// Prefer a writer worker thread when writes can block:
// terminal_write enqueues, worker does the blocking write.
// (drop sender on shutdown; worker exits naturally)
```

This prevents a blocked PTY write or an IPC/bus probe from stalling the threads that handle UI actions or incoming commands, and it avoids deadlocks/starvation caused by holding locks during slow operations.