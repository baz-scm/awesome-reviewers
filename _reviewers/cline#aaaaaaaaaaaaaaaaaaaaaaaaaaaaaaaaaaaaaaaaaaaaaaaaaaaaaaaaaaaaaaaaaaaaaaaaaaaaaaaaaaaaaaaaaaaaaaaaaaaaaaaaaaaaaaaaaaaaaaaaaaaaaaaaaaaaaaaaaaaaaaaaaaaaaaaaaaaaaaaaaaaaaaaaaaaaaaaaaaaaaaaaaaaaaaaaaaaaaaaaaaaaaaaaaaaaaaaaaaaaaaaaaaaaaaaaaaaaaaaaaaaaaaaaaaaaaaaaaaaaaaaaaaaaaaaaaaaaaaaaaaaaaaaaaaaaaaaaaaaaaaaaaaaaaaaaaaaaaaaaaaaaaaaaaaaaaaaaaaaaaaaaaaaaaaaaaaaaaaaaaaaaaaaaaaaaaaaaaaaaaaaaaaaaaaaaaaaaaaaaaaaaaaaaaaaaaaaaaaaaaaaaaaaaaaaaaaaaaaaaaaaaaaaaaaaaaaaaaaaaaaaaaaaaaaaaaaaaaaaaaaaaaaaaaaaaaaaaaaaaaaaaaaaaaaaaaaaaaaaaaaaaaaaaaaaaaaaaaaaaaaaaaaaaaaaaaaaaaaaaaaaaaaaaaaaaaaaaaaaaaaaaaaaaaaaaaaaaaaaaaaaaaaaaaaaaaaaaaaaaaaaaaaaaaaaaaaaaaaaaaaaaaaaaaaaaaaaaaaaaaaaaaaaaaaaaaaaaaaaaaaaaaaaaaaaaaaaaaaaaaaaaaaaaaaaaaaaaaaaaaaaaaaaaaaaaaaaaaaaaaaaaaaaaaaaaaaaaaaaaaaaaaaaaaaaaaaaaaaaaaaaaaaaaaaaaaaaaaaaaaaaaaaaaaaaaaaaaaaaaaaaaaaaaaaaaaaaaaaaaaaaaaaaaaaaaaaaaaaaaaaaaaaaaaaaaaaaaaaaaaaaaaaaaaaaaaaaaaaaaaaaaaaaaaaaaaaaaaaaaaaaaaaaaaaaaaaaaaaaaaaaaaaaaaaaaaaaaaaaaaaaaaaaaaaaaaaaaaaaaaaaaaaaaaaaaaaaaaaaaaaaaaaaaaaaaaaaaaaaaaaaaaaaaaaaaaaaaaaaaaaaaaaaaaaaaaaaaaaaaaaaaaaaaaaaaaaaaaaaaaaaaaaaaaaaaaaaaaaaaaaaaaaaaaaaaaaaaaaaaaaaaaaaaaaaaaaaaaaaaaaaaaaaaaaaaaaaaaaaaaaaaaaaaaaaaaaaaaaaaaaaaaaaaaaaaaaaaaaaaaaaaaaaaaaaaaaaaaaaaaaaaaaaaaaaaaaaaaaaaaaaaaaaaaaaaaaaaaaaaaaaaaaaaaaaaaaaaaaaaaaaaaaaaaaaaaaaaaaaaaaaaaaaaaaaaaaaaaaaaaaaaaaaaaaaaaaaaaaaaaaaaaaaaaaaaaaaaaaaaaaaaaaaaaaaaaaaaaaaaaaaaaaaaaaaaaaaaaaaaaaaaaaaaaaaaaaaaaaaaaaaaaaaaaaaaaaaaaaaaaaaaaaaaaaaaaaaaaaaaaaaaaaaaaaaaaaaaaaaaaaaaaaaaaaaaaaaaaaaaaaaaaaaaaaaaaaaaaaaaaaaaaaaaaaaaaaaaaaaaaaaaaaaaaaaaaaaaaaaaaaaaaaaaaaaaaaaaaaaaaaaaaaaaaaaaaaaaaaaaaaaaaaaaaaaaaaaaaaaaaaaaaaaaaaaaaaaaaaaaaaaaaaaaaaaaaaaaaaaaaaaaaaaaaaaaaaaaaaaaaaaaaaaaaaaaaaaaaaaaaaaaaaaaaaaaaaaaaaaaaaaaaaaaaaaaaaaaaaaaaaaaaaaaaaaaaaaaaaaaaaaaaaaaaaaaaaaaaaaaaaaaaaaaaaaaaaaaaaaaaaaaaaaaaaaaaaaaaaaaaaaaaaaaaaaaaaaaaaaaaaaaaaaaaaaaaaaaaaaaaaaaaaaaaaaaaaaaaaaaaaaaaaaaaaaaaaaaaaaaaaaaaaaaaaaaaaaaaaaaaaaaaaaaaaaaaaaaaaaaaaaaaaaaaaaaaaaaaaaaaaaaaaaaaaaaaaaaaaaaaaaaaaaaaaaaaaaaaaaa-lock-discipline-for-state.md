---
title: Lock discipline for state
description: 'When multiple threads share mutable state behind locks, design for both
  liveness and correctness, not just mutual exclusion:


  1. Keep critical sections short. Never do blocking I/O (writes, process spawn, DBus/network
  calls) while holding a lock other operations need. If a write can block indefinitely
  (e.g. a PTY write to a stalled shell), move it off the...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70965
---

When multiple threads share mutable state behind locks, design for both liveness and correctness, not just mutual exclusion:

1. Keep critical sections short. Never do blocking I/O (writes, process spawn, DBus/network calls) while holding a lock other operations need. If a write can block indefinitely (e.g. a PTY write to a stalled shell), move it off the lock-holding thread entirely — hand it to a dedicated worker fed by a channel, and have the caller only enqueue:
```rust
// Bad: terminal_write blocks the IPC command thread under the sessions lock.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(data.as_bytes())?;

// Good: enqueue to a per-session writer thread; the lock is only used
// to clone a cheap handle (sender), never held across the blocking call.
sessions.get(&id).unwrap().tx.send(data)?;
```

2. When more than one lock can be held together, document and enforce a single, fixed acquisition order (e.g. "`process` may be held while acquiring `ws_endpoint`, never the reverse") so no two code paths can deadlock by taking them in opposite orders.

3. Treat an unlocked check as advisory only. State can change between the check and the lock being acquired (TOCTOU), so re-validate any invariant you rely on (a shutdown flag, "is this still the active session") immediately after acquiring the lock, before acting on it.

4. Protect shared state from stale concurrent callbacks. A background thread, reader, or timer callback may fire after the resource it refers to has already been replaced or removed. Tag resources with a generation counter or unique id, and before a background thread mutates shared state, verify under the lock that the id/generation it captured still matches the current one — otherwise skip the update instead of clobbering newer state:
```rust
// A reader thread must not remove a session that was replaced after it
// captured `id`; compare the generation it was spawned with.
if sessions.get(&id).map(|s| s.generation) == Some(my_generation) {
    sessions.remove(&id);
}
```

5. For races that cannot be resolved cleanly (e.g. a probe racing a timeout), pick the resolution that fails toward the cheaper, more recoverable outcome, and record that reasoning in a comment next to the timeout/constant so future changes don't silently flip it.

Applying these rules prevents stalled IPC/UI threads, deadlocks from inconsistent lock ordering, and subtle races where late callbacks overwrite fresher state.