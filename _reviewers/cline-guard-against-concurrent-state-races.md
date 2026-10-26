---
title: Guard against concurrent state races
description: 'When shared state is mutated by multiple threads, background readers/waiters,
  or async callbacks, treat every check-then-act sequence as a potential race and
  design for it explicitly:'
repository: cline/cline
label: Concurrency
language: Rust
comments_count: 5
repository_stars: 70886
---

When shared state is mutated by multiple threads, background readers/waiters, or async callbacks, treat every check-then-act sequence as a potential race and design for it explicitly:

1. Re-validate state after acquiring a lock, not before. A "shutting down" or "already running" flag checked outside a lock can go stale by the time the lock is taken; recheck it inside the critical section before spawning, replacing, or mutating.

2. Tag long-lived resources (child processes, sessions, PTYs) with a generation/identity marker when they can be replaced while a background thread still references the old instance. A waiter or reader thread that finishes late must compare its captured id/generation against the current one before removing or clearing shared state, so a stale completion from a replaced resource cannot clobber its successor:
```rust
let generation = NEXT_GENERATION.fetch_add(1, Ordering::Relaxed);
// ... later, in the waiter thread:
if map.get(&id).is_some_and(|s| s.generation == generation) {
    map.remove(&id); // only remove if we still own this slot
}
```

3. When two locks must ever be held together, pick and document one fixed acquisition order (e.g., "process before ws_endpoint, never the reverse") and ensure every code path, including teardown/`Drop`, follows it to avoid deadlocks.

4. Prefer holding a single lock across an entire check-and-act operation (e.g., "is a process already running? if not, spawn one") over separate lock/unlock steps, so concurrent callers serialize instead of racing to spawn duplicates or overwrite each other's work. For TOCTOU-sensitive operations like replacing an installed binary, re-verify the precondition (e.g., version/epoch) under the same lock immediately before the destructive action.

5. When a timeout or a race between threads must resolve to one of two outcomes and both carry risk, choose the direction that fails safe for the *more likely* scenario, and record that reasoning in a comment so a future change doesn't silently flip it. Add a test that locks in the chosen behavior for the ambiguous case.

Applying these practices prevents duplicate spawns, resource leaks, deadlocks, and stale background work from corrupting state owned by its replacement.