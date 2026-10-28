---
title: Bound concurrent waits
description: Any operation that crosses a thread, process, or actor boundary — joining
  a thread, acquiring a lock, waiting on a channel, reading/writing a socket, or waiting
  for an external process — must be bounded by an explicit deadline or capacity limit,
  so a stalled peer, hung descendant process, or full queue can never stall the owning
  loop or other concurrent...
repository: ogulcancelik/herdr#canary966c66ad
label: Concurrency
language: Rust
comments_count: 12
repository_stars: 46332
---

Any operation that crosses a thread, process, or actor boundary — joining a thread, acquiring a lock, waiting on a channel, reading/writing a socket, or waiting for an external process — must be bounded by an explicit deadline or capacity limit, so a stalled peer, hung descendant process, or full queue can never stall the owning loop or other concurrent callers indefinitely.

In practice:
- Replace blocking joins/recvs with `recv_timeout`/deadline-based polling, and when a bounded wait expires, detach or cancel the work rather than blocking forever (e.g. dropping reader threads instead of `join()`ing them after a kill, because a `ProxyCommand` descendant can keep the pipe open).
- Give related operations that must complete together (e.g. a datagram send plus barrier wait, or several retries after `EINTR`) one shared deadline, not a fresh timeout per step, so retries can't silently extend the total wait.
- Cap concurrently spawned threads/workers/permits (e.g. a fixed worker pool, a bounded semaphore of completion waiters) instead of spawning without limit per request; reject or queue new work when the cap is hit rather than letting resource usage grow unbounded.
- When a slow consumer or hung resource makes a wait unavoidable (shutdown flushing a write, handing off a PTY), make the bound and its consequences an explicit, tested contract (e.g. "flush this one write before teardown, but don't guarantee draining an arbitrarily large queue") rather than an implicit hope.
- Only add bounds/backpressure where there's a demonstrated resource-exhaustion risk; don't add arbitrary limits without evidence, since overly aggressive bounds can be as harmful as none.
- When a true bound is impossible because the underlying OS/API offers no atomic check-then-act primitive, narrow the window as much as possible (e.g. re-reading state immediately before injecting input) and explicitly document the accepted residual race instead of leaving it unbounded or unexamined.

Example pattern for a bounded cross-process wait with a shared deadline:
```rust
let deadline = Instant::now() + TIMEOUT;
loop {
    match try_operation() {
        Ok(result) => return Ok(result),
        Err(e) if e.kind() == ErrorKind::Interrupted => {}
        Err(e) if e.kind() == ErrorKind::WouldBlock => {}
        Err(e) => return Err(e),
    }
    if Instant::now() >= deadline {
        return Err(io::Error::new(ErrorKind::TimedOut, "operation timed out"));
    }
    sleep(POLL_INTERVAL);
}
```