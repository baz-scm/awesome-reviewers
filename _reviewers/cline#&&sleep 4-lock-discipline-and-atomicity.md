---
title: Lock discipline and atomicity
description: 'When sharing mutable state across threads, keep critical sections minimal
  and race-free:


  1. Never perform blocking I/O (writes, process spawn/wait, network calls) while
  holding a lock that other threads need for liveness. Either clone the resource under
  the lock and release it before blocking (e.g., clone a writer handle, then `write_all`
  outside the...'
repository: cline/cline#&&sleep 4
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70980
---

When sharing mutable state across threads, keep critical sections minimal and race-free:

1. Never perform blocking I/O (writes, process spawn/wait, network calls) while holding a lock that other threads need for liveness. Either clone the resource under the lock and release it before blocking (e.g., clone a writer handle, then `write_all` outside the lock), or move the blocking work to a dedicated thread fed by a channel so the IPC/command thread only enqueues work and returns immediately.

2. Treat "check" and "act" as one atomic unit by performing both under the same lock, right next to each other. A check done before acquiring the lock (or before the final mutation) is a TOCTOU race: another thread can change state in the gap. Examples: recheck a shutdown/cancellation flag immediately before spawning a new process (not just before taking the lock), and recheck an installed version/build epoch while still holding the installation lock, immediately before overwriting the executable, so a concurrent installer cannot win a race against a stale check.

3. When more than one lock protects related state, document and enforce a single, fixed acquisition order (e.g., "`process` may be held while acquiring `ws_endpoint`, never the reverse") and ensure every code path, including teardown/`Drop`, follows it. Prefer collapsing related state into fewer locks when the ordering becomes hard to reason about.

4. When concurrent threads share a mutable collection keyed by an id that can be reused or replaced, protect against stale writers by tagging entries with a generation/version and verifying it still matches before removing or mutating the entry, rather than assuming the first id-based lookup is still valid.

Example pattern for not blocking the command thread:
```rust
// Bad: holds the sessions lock during a potentially blocking write.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(data)?;

// Good: hand the write off to a dedicated per-session thread via a channel.
let sender = {
    let sessions = state.sessions.lock().unwrap();
    sessions.get(&id).unwrap().sender.clone()
};
sender.send(data)?; // never blocks the caller on shell I/O
```

Applying these rules prevents deadlocks, stalled UI/IPC threads, and subtle races where a concurrent actor undoes or duplicates work performed between a check and its corresponding action.