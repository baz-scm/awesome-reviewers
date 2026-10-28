---
title: Lock ordering and rechecks
description: 'When multiple mutexes or shared-state checks are involved, (1) document
  and consistently follow one fixed lock-acquisition order everywhere that touches
  more than one lock, so no code path can deadlock by nesting locks in the opposite
  order, e.g.:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70967
---

When multiple mutexes or shared-state checks are involved, (1) document and consistently follow one fixed lock-acquisition order everywhere that touches more than one lock, so no code path can deadlock by nesting locks in the opposite order, e.g.:

```rust
/// Lock order: `process` may be held while acquiring `ws_endpoint`, never
/// the reverse. Anything that touches both must nest in that order or take
/// them strictly sequentially.
struct State {
    ws_endpoint: Mutex<Option<String>>,
    process: Mutex<Option<Child>>,
}
```

(2) Never trust a condition checked before or outside a lock as still true once you're inside it — another thread may have changed the state in the meantime (classic TOCTOU). Re-check the invariant immediately after acquiring the lock and right before performing the irreversible action, not just once up front:

```rust
fn ensure_started(state: &State, spawn: impl FnOnce() -> Result<Child, String>) -> Result<(), String> {
    let mut guard = state.process.lock().unwrap();
    // Re-check under the lock: shutdown may have been triggered between the
    // caller's earlier unlocked check and this point.
    if state.is_shutting_down() {
        return Ok(());
    }
    ...
}
```
This same pattern applies to any "check-then-act" sequence guarding a mutating side effect (e.g., re-validating a version/epoch immediately before overwriting a file while holding the installation lock), and to disambiguating stale references by identity (e.g., comparing a tracked child's pid before clearing shared state, so a late callback from a replaced/reaped process can't clobber state its successor already set).

(3) When a thread that must stay responsive (UI/main thread) needs to perform a potentially slow or blocking call, run it on a separate thread with a bounded timeout, and pick a safe, non-destructive fallback for the ambiguous "timed out" case rather than assuming the worst-case outcome (e.g., prefer leaving the app running over quitting it when a slow IPC probe can't be distinguished from "no listener").

Apply this standard whenever introducing or modifying code that holds multiple locks, performs check-then-act sequences on shared/mutable state, or crosses thread boundaries with a timeout.