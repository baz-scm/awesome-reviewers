---
title: Lock scope and recheck
description: Keep critical sections minimal and never perform blocking work (I/O writes,
  process spawn/kill/wait, network or D-Bus calls) while holding a lock that other
  threads need for quick state updates. A blocked write or RPC inside a mutex stalls
  every other caller of that lock, including the UI/command thread. Instead, hand
  blocking work off to a dedicated thread...
repository: "cline/cline\r\n"
label: Concurrency
language: Rust
comments_count: 5
repository_stars: 70946
---

Keep critical sections minimal and never perform blocking work (I/O writes, process spawn/kill/wait, network or D-Bus calls) while holding a lock that other threads need for quick state updates. A blocked write or RPC inside a mutex stalls every other caller of that lock, including the UI/command thread. Instead, hand blocking work off to a dedicated thread fed by a channel, and only take the lock briefly to enqueue work or clone a handle:

```rust
// Bad: write_all under the lock can block the IPC thread indefinitely.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(&data)?;

// Good: enqueue to a writer thread; the lock is only held to send.
let input = { state.sessions.lock().unwrap().get(&id).unwrap().input.clone() };
input.send(data).ok();
```

When a check-then-act sequence spans an unlocked read and a later lock acquisition (e.g. "is the backend shutting down?" before spawning, or "is the installed build newer?" before replacing a file), re-verify the condition again immediately after acquiring the lock and right before the mutating action. The window between the initial check and taking the lock is exactly where another thread can invalidate the result.

For long-lived background threads/callbacks that eventually mutate shared state (a PTY reader removing its session, a sidecar's stdout reader clearing an endpoint, a retry respawning a child), tag the resource with a generation id or pid and verify the thread still owns the current instance before writing — a late callback from a replaced or already-superseded resource must never clobber state belonging to its successor.

Finally, when probing an external or potentially slow resource (a D-Bus service, a subprocess) from a thread that must stay responsive (GTK main thread, IPC command thread), run the probe on a background thread and bound the wait with a timeout, choosing a safe default behavior if the timeout is reached. Document lock ordering explicitly when more than one lock can be held together, and always acquire locks in the same, documented order across the codebase to avoid deadlocks.