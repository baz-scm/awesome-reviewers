---
title: Guard shared state from async races
description: 'When multiple threads or async tasks share mutable state (sessions,
  process handles, endpoints), design explicitly for races between concurrent operations
  and stale completions, not just for mutual exclusion:'
repository: cline/cline;
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70964
---

When multiple threads or async tasks share mutable state (sessions, process handles, endpoints), design explicitly for races between concurrent operations and stale completions, not just for mutual exclusion:

1. Never perform blocking I/O while holding a lock that other critical paths need. A blocked `write_all`/`read` under a shared mutex can stall unrelated callers (e.g. an IPC command thread trying to kill a session). Offload blocking work to a dedicated thread fed by a channel, and only take the lock briefly to enqueue/clone a handle:
```rust
// Writer thread owns the blocking write; the command handler only enqueues.
let (input, input_rx) = channel::<Vec<u8>>();
thread::spawn(move || {
    for chunk in input_rx {
        if writer.write_all(&chunk).is_err() { break; }
    }
});
```

2. Tag long-lived resources (sessions, spawned processes) with a generation id or other identity check, and verify that identity under the lock before a background thread mutates shared state on completion (removing an entry, clearing an endpoint). This prevents a stale reader/waiter from a superseded instance clobbering state that a newer instance already established:
```rust
if map.get(&id).is_some_and(|s| s.generation == generation) {
    map.remove(&id); // only remove if we still own this slot
}
```

3. When a struct holds multiple mutexes, document and enforce a single, consistent lock acquisition order (e.g. "`process` may be held while acquiring `ws_endpoint`, never the reverse") so that no code path can deadlock by nesting locks in the opposite order. Any function touching more than one lock must follow this order or take the locks strictly sequentially.

Apply these rules whenever introducing shared state across threads: prefer channels/dedicated workers over blocking under a lock, verify ownership/generation before mutating shared maps from async callbacks, and keep lock ordering documented and consistent.