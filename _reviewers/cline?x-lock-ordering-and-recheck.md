---
title: Lock ordering and recheck
description: When shared mutable state is guarded by multiple locks or flags, make
  the concurrency contract explicit and defend against races at the point of action,
  not just at the point of initial check.
repository: cline/cline?x
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70983
---

When shared mutable state is guarded by multiple locks or flags, make the concurrency contract explicit and defend against races at the point of action, not just at the point of initial check.

1. Document and enforce a fixed lock acquisition order whenever more than one mutex protects related state (e.g. "lock A may be held while acquiring lock B, never the reverse"). Any code path that touches both resources must follow that order or take the locks strictly sequentially, otherwise deadlocks become possible as the code grows.

2. Never trust a condition checked before a lock was acquired. An unlocked pre-check (e.g. "is the service already shutting down?") is only an optimization to skip unnecessary locking; the authoritative check must happen again immediately after the lock is taken and immediately before the action that depends on it (spawning a process, replacing an installed binary, publishing an endpoint). For example:

```rust
// Cheap early-out, not authoritative.
if state.is_shutting_down() { return Ok(()); }

let guard = state.process.lock()?;
// Re-check under the lock: a concurrent stop() may have flipped the
// flag and taken this same lock between the check above and here.
if state.is_shutting_down() { return Ok(()); }
// ...spawn/replace happens here, still holding the lock...
```
The same pattern applies to version/epoch checks before overwriting an installed artifact: re-read the installed version while holding the installation lock, right before the write, instead of relying on an earlier check.

3. When tagging asynchronous results (callbacks, reader threads, respawned children) with an identity such as a PID, verify that identity still matches the currently tracked resource before applying the result, so a stale update from a superseded instance cannot clobber state set by its successor.

4. Any blocking call made from a latency-sensitive thread (UI/main thread, shutdown handler) must be bounded with an explicit timeout, run off that thread, and have a documented, safe default behavior for the timeout case. Justify why the timeout and its fallback are safe (e.g. "a bus daemon rejects a missing service immediately, so only a slow-but-present service reaches the timeout, and falling back to the pre-existing behavior there is intentional").

Apply this checklist to any new shared-state code: define lock order, re-validate under the lock, validate the identity of async results, and bound blocking probes with a documented timeout and fallback.</description>
</invoke>
