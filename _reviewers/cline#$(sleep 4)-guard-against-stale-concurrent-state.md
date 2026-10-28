---
title: Guard against stale concurrent state
description: 'When multiple threads, async callbacks, or respawned resources (child
  processes, PTY sessions, reader/writer threads) can race to mutate shared state,
  make staleness impossible to act on rather than merely unlikely:'
repository: cline/cline#$(sleep 4)
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70978
---

When multiple threads, async callbacks, or respawned resources (child processes, PTY sessions, reader/writer threads) can race to mutate shared state, make staleness impossible to act on rather than merely unlikely:

- Tag each live resource with an identity token (a generation counter or PID) when it's created, and have any background thread or callback that later wants to mutate shared state re-check that its token still matches the current one before acting. This stops a late exit/EOF from a previous shell, child process, or reader thread from evicting or overwriting state that already belongs to its successor. Example pattern:
```rust
let generation = NEXT_GENERATION.fetch_add(1, Ordering::Relaxed);
sessions.insert(id, Session { generation, .. });
// later, in the waiter thread:
if map.get(&id).is_some_and(|s| s.generation == generation) {
    map.remove(&id);
}
```
- When a flag like `shutting_down` or `is_shutting_down()` can flip concurrently with a check-then-act sequence, check it once before acquiring the lock (fast path) and check it again after acquiring the lock, immediately before mutating state. The second check closes the window where the flag flipped while the lock was being awaited.
- Document lock acquisition order explicitly in a comment on the struct (e.g., "`process` may be held while acquiring `ws_endpoint`, never the reverse") so that any code touching multiple locks follows the same order and deadlocks are structurally avoided rather than caught by luck.
- When a race is resolved via a timeout (e.g., probing an external service with `recv_timeout`), don't just pick an arbitrary default — identify which of the two possible wrong outcomes is more likely and less costly to recover from, pick the resolution that favors the safer outcome, and record that reasoning in a comment so it isn't "fixed" in the wrong direction later.

Applying these patterns prevents an entire class of bugs where a resource is respawned, reloaded, or shut down, but a stale thread or callback from the previous generation still manages to clobber current state, kill a fresh process, or leak a session.