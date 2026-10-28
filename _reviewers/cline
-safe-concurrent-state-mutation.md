---
title: Safe concurrent state mutation
description: When multiple threads can read, write, or replace shared state, design
  for interleavings explicitly rather than assuming operations complete in the order
  they were started.
repository: 'cline/cline

  '
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70942
---

When multiple threads can read, write, or replace shared state, design for interleavings explicitly rather than assuming operations complete in the order they were started.

1. Never hold a lock across a blocking call. Take the lock only long enough to extract or hand off a handle, then release it before doing I/O. If the blocking operation itself can stall a thread other code depends on (an IPC command handler, a GTK/UI main thread), move that operation to a dedicated worker fed by a channel, so the caller only enqueues work and returns immediately:
```rust
// Bad: lock held while write_all can block indefinitely.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(&data)?;

// Good: command thread only enqueues; a dedicated writer thread blocks instead.
let input = { state.sessions.lock().unwrap().get(&id).unwrap().input.clone() };
input.send(data).ok();
```

2. Protect against stale completions from background threads or timed-out probes overwriting newer state. When an entry can be replaced or removed while an older async task (reader, waiter, timer) is still in flight, tag each instance with a generation/version id and have the background task check that tag still matches before mutating shared state:
```rust
if map.get(&id).is_some_and(|s| s.generation == my_generation) {
    map.remove(&id);
}
```

3. For operations that can hang indefinitely (a D-Bus call, a subprocess probe), run them off the thread that must stay responsive and bound the wait with a timeout; pick the safe default behavior for the timeout/failure case rather than assuming success or failure.

4. For check-then-act sequences across restarts or processes (e.g. "is the installed version newer before I overwrite it?"), re-validate the condition while holding the exclusive lock/mutex immediately before mutating, not earlier — the state may have changed between the check and the acquisition of the lock.

Apply these patterns whenever shared mutable state is touched by more than one thread, IPC handler, or async callback: minimize critical sections, never block while holding a lock, tag in-flight work so late completions can't clobber newer state, and recheck invariants at the point of mutation.