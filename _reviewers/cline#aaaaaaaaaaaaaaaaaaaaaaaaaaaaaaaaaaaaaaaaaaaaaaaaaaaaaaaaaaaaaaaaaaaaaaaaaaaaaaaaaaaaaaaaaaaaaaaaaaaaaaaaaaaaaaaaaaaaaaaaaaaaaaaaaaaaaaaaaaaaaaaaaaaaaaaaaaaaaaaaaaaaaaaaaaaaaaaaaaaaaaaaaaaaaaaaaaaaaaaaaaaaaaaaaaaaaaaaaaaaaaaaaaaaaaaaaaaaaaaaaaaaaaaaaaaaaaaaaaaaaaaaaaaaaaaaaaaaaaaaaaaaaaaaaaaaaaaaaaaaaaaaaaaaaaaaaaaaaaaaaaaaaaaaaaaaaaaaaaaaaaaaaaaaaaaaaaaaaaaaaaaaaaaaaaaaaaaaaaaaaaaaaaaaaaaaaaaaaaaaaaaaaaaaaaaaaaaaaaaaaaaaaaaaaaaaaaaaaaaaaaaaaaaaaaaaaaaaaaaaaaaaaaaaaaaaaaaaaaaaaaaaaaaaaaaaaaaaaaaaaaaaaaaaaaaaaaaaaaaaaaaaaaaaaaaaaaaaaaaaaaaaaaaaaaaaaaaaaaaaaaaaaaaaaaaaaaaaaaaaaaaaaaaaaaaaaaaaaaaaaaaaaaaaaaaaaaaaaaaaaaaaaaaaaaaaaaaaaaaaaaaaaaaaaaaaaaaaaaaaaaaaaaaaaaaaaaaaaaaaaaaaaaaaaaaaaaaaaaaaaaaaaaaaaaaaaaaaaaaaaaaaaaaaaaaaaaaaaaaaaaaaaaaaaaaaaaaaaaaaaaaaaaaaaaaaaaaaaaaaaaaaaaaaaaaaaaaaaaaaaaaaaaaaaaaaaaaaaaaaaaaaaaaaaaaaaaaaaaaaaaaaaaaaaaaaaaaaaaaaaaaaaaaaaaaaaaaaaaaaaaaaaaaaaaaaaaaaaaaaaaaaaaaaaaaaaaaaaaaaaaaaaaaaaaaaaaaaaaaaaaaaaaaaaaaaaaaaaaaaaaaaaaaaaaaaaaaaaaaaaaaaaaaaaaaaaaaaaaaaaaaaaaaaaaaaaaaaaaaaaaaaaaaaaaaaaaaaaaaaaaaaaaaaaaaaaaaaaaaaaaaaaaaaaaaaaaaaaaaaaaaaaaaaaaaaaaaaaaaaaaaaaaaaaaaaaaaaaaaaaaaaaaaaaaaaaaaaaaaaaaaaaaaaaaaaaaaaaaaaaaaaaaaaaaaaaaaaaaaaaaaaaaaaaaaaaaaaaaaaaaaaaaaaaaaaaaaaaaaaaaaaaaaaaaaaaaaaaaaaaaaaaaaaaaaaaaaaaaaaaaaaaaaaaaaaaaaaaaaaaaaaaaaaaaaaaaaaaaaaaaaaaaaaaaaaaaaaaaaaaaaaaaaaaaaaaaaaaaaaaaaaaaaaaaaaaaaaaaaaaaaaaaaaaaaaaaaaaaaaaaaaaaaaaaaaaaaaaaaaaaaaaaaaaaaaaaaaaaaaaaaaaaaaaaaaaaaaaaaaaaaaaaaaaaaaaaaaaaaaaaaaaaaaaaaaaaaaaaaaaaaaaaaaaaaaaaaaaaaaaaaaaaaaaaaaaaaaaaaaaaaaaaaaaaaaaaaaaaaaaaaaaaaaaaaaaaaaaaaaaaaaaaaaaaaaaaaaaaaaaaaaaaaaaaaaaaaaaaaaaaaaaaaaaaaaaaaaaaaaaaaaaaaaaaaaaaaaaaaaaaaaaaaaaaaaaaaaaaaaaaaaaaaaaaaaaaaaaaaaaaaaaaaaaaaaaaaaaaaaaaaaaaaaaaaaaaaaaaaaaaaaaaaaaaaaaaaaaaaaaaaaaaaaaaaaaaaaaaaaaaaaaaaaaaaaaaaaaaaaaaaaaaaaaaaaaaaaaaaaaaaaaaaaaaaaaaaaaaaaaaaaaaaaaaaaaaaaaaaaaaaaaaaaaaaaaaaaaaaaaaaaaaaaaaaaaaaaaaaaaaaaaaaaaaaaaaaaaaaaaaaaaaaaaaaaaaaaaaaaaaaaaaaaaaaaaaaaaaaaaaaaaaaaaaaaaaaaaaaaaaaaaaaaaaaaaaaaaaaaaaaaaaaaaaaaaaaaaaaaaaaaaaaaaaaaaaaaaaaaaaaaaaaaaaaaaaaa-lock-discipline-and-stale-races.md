---
title: Lock discipline and stale races
description: Shared state protected by a mutex must only ever be held briefly to read
  or mutate that state — never across a blocking call. If a blocking operation (a
  PTY write, a process wait, a D-Bus/network probe) is unavoidable, move it to a dedicated
  worker thread fed by a channel, and have the lock-holding side only enqueue work
  or clone a handle before releasing...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70976
---

Shared state protected by a mutex must only ever be held briefly to read or mutate that state — never across a blocking call. If a blocking operation (a PTY write, a process wait, a D-Bus/network probe) is unavoidable, move it to a dedicated worker thread fed by a channel, and have the lock-holding side only enqueue work or clone a handle before releasing the lock. A command handler or UI thread that invokes a potentially slow external call should never wait on it directly; instead spawn it on its own thread and bound the wait with `recv_timeout`, falling back to a safe default if it overruns.

When a resource can be replaced or torn down while background work (readers, waiters, exit handlers) is still in flight for the old instance, tag each instance with a generation counter or process id and have any completion handler re-check that tag under the lock before mutating shared state. This prevents a stale callback from a superseded resource from evicting or overwriting its successor's entry — e.g. a reader thread for a respawned terminal session must not remove the new session just because the old generation exited late.

Any "check, then act" sequence that spans an unlocked read followed by a locked mutation (e.g. checking a shutdown flag before taking a lock to spawn a process) must re-validate the condition again after the lock is acquired, since the state can change in the gap between the check and the acquisition.

When a type holds multiple mutexes, document and enforce one fixed acquisition order (e.g. "the process lock may be held while acquiring the endpoint lock, never the reverse") so unrelated call paths cannot deadlock by acquiring them in different orders. Example of the enqueue pattern instead of holding a lock during a blocking write:

```rust
// WRONG: holds the sessions lock across a blocking write_all
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(&data)?;

// RIGHT: lock only to enqueue; a dedicated writer thread drains the channel
let input = {
    let sessions = state.sessions.lock().unwrap();
    sessions.get(&id).unwrap().input.clone()
};
input.send(data).ok();
```