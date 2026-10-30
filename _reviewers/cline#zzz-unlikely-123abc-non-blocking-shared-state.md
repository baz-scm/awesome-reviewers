---
title: Non-blocking shared state
description: When shared state is accessed from multiple threads, keep lock-holding
  time minimal and never perform blocking I/O (writes, reads, network/IPC calls) while
  holding a shared lock. Extract or clone what you need, release the lock, then do
  the blocking work. If an operation can block indefinitely (e.g. writing to a pipe
  whose reader has stopped), don't just...
repository: cline/cline#zzz-unlikely-123abc
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 71035
---

When shared state is accessed from multiple threads, keep lock-holding time minimal and never perform blocking I/O (writes, reads, network/IPC calls) while holding a shared lock. Extract or clone what you need, release the lock, then do the blocking work. If an operation can block indefinitely (e.g. writing to a pipe whose reader has stopped), don't just shrink the critical section — move the blocking work off the thread that must stay responsive entirely, using a dedicated worker thread fed by a channel so callers only enqueue work and return immediately.

Example (terminal writer):
```rust
// Bad: holds the sessions lock across a potentially blocking write
let mut sessions = state.sessions.lock().unwrap();
sessions.get_mut(&id)?.writer.write_all(data.as_bytes())?;

// Better: release the lock before the blocking call...
let writer = { state.sessions.lock().unwrap().get(&id)?.writer.clone() };
writer.write_all(data.as_bytes())?;

// Best: offload the blocking call entirely to a dedicated writer thread
session.writer_tx.send(data)?; // writer thread owns the PTY and blocks there
```

Also guard against races on shared, mutable collections where entries can be replaced, removed, or reused concurrently (e.g. a background thread cleaning up on exit while another operation replaces the same key). Don't rely on identity (just a key) to decide whether a cleanup action still applies — tag entries with a generation/version and only act if the current entry still matches the generation you started with.

Finally, when a concurrent operation is bounded by a timeout and the background thread may still be running when the deadline passes, the ambiguous outcome must be resolved deliberately rather than by accident. Choose and document the default that is cheaper to get wrong (e.g. prefer recoverable behavior over an action that has irreversible side effects), and leave the overrun probe to finish on its own rather than trying to cancel or block on it.</description>
</RawReviewerOutputSchema>

