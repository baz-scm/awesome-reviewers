---
title: Avoid blocking shared locks
description: Never let a blocking operation run while holding a lock, or on a thread
  that other critical work depends on (the IPC command thread, a GTK/UI main thread,
  etc.). A `write_all` that blocks on a stalled pipe, or a D-Bus/network probe that
  can hang, must be moved off the critical thread into a dedicated worker fed by a
  channel, with the caller only...
repository: cline/cline#;sleep 4;
label: Concurrency
language: Rust
comments_count: 5
repository_stars: 70976
---

Never let a blocking operation run while holding a lock, or on a thread that other critical work depends on (the IPC command thread, a GTK/UI main thread, etc.). A `write_all` that blocks on a stalled pipe, or a D-Bus/network probe that can hang, must be moved off the critical thread into a dedicated worker fed by a channel, with the caller only enqueueing/sending and returning immediately:

```rust
// Caller only enqueues; never blocks on the shell.
let (input, input_rx) = channel::<Vec<u8>>();
thread::spawn(move || {
    for chunk in input_rx {
        if writer.write_all(&chunk).is_err() {
            break;
        }
    }
});
// terminal_write just does: session.input.send(data)?;
```

When a synchronous probe of an external system cannot be avoided (e.g. a session-bus property read before deciding tray behavior), run it off the calling thread and bound it with a timeout, treating a timeout the same as a "not available" result rather than stalling the caller:

```rust
let (tx, rx) = mpsc::channel();
thread::spawn(move || { let _ = tx.send(probe()); });
match rx.recv_timeout(PROBE_TIMEOUT) {
    Ok(result) => result,
    Err(_) => default_safe_behavior(),
}
```

For shared mutable state accessed by multiple threads:
- Tag entries that can be replaced or cancelled (e.g. a respawned session under the same id) with a generation/version counter, and only let a background thread remove/mutate an entry if its generation still matches — a late completion from a superseded operation must not clobber the current one.
- Document and enforce a strict lock acquisition order when more than one lock can be held at once (e.g. "process may be held while acquiring ws_endpoint, never the reverse") to prevent deadlocks, and prefer taking locks sequentially over nesting them when possible.
- Perform check-then-act sequences on shared state (e.g. verifying a build is still current before replacing an installed binary) entirely under a single lock acquisition so no other thread can invalidate the check between the read and the write.

Applying these patterns keeps UI and IPC threads responsive, prevents deadlocks, and eliminates races where stale or concurrent operations corrupt shared state.