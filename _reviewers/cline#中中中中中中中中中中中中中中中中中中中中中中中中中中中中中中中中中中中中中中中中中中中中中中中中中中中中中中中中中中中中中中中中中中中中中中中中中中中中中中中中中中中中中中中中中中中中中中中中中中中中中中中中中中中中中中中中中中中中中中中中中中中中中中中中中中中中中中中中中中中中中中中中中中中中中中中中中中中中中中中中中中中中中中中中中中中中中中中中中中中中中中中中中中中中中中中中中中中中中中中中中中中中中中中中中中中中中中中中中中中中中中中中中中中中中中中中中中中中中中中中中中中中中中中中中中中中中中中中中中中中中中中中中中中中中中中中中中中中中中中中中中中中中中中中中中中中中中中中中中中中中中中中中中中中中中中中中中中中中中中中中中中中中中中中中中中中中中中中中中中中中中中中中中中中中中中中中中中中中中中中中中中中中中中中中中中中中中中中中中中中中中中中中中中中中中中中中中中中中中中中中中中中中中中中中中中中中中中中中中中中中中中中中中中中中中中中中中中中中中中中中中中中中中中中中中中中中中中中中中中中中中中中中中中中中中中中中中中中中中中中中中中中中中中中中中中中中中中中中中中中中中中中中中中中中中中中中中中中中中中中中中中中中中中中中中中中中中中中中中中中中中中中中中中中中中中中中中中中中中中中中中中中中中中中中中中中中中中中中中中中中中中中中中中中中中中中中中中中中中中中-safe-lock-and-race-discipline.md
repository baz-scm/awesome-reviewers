---
title: Safe lock and race discipline
description: 'Treat locks as protecting only in-memory state, never as a way to serialize
  blocking work. Keep critical sections minimal: acquire a lock, read/mutate shared
  state, release it — never call blocking I/O (writes, process spawn/kill/wait, network
  calls) while a lock is held, since a stalled call then stalls every other thread
  waiting on that lock. If a...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70984
---

Treat locks as protecting only in-memory state, never as a way to serialize blocking work. Keep critical sections minimal: acquire a lock, read/mutate shared state, release it — never call blocking I/O (writes, process spawn/kill/wait, network calls) while a lock is held, since a stalled call then stalls every other thread waiting on that lock. If a blocking operation is required, hand it off to a dedicated worker fed by a channel so the lock holder only enqueues work instead of performing it:

```rust
// Bad: write_all can block while holding `sessions`, stalling kill/exit too.
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id).unwrap().writer.write_all(&data)?;

// Good: the lock only clones a handle; the blocking write happens off-thread.
let input = {
    let sessions = state.sessions.lock().unwrap();
    sessions.get(&id).unwrap().input.clone()
};
input.send(data)?; // a dedicated writer thread drains this channel
```

When an operation touches more than one lock, document and enforce a single fixed acquisition order everywhere (e.g. "`process` may be held while acquiring `ws_endpoint`, never the reverse") to rule out deadlocks.

Any check used to decide whether to act (is a process still shutting down? is this the file we should replace? is this session still current?) must be re-verified *after* the lock is acquired and immediately before acting, not just before trying to acquire it — otherwise another thread can invalidate the check in the gap (classic TOCTOU). For long-lived async work (background threads, respawned processes, replaced sessions), tag each instance with a generation/id and have completions check that the shared slot still belongs to their generation before mutating or removing it, so a stale completion from a superseded instance cannot corrupt or evict the current one. Apply the same discipline to ordering dependent async steps across process boundaries (e.g. a reload must wait for a kill-all acknowledgment before spawning a replacement) rather than assuming they race safely.