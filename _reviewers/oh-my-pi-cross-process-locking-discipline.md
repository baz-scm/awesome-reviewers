---
title: Cross-process locking discipline
description: When mutating shared on-disk state that other processes or threads may
  touch concurrently (worktree registrations, refs, config files), always serialize
  the check-then-act sequence behind an explicit, cross-process lock, and never let
  cleanup code interfere with another holder's in-progress work.
repository: can1357/oh-my-pi
label: Concurrency
language: Rust
comments_count: 6
repository_stars: 37317
---

When mutating shared on-disk state that other processes or threads may touch concurrently (worktree registrations, refs, config files), always serialize the check-then-act sequence behind an explicit, cross-process lock, and never let cleanup code interfere with another holder's in-progress work.

Concretely:
- Prefer the underlying tool's native atomic primitives when available (e.g. `git update-ref --no-deref` for compare-and-swap on a ref) instead of reimplementing read-modify-write logic yourself; this guarantees a concurrent writer is never silently overwritten.
- When you must implement your own lock, use the strongest primitive the filesystem supports (e.g. `File::lock`), but provide a correct fallback (exclusive-create claim files) for filesystems without lock support (NFSv3, etc.), and make sure the fallback is itself race-free.
- Acquire the lock *before* checking preconditions, and keep it held across the check and the mutation. After releasing a lock (or waiting for another writer's lock to clear), re-verify the state before performing any dependent cleanup — don't act on a stale snapshot taken before the lock was released:
  ```rust
  // Bad: state may change between check and cleanup
  delete_ref(name)?;
  remove_config_section(name); // ref might have been recreated by now

  // Good: re-check under the lock immediately before mutating
  let _lock = acquire_config_lock(path)?;
  if ref_absent(name)? {
      remove_config_section(name);
  }
  ```
- Never delete, unlock, or otherwise finalize something you don't own or that is still in progress elsewhere: a prune/cleanup routine must skip entries marked as locked or still-being-set-up by another process, and exit/cleanup handlers must only release locks or remove claim files for operations that have actually completed (wait with a bounded timeout for in-flight work, don't force-release it).
- When an operation partially fails and must roll back, order the rollback steps so no other process can ever observe a half-finished, inconsistent state (e.g. remove the piece that makes an entry "listed" last, after everything it depends on is already gone, so a concurrent reader either sees the whole entry or nothing).
- Add tests that simulate concurrent holders (another process holding the lock/claim, a lock released mid-operation, a process killed while holding a claim) to prove the race is actually closed, not just the happy path.