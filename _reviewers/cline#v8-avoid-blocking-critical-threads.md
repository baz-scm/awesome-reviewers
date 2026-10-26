---
title: Avoid blocking critical threads
description: When concurrency involves locks, IPC, or UI/close handlers, ensure no
  potentially blocking I/O or long waits run while holding a lock or on a latency-sensitive
  thread. Also make cleanup race-safe.
repository: cline/cline#v8
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70867
---

When concurrency involves locks, IPC, or UI/close handlers, ensure no potentially blocking I/O or long waits run while holding a lock or on a latency-sensitive thread. Also make cleanup race-safe.

Apply these rules:
- Keep lock scope minimal: take the lock only to fetch/clone handles; drop it before any blocking call.
- Offload blocking I/O to a worker: have command handlers enqueue work to a per-session/per-resource thread via an `mpsc` channel, so the handler stays responsive.
- Prevent stale lifecycle updates: if sessions can be replaced/reused, attach an ownership token (e.g., generation/id) and only remove/cleanup if the token still matches.
- If using timeouts in concurrency (e.g., probing external state), run the probe off-thread and explicitly document which outcome you prefer when timeout is ambiguous.

Example pattern (writer thread + enqueue):
```rust
// Handler: enqueue only (non-blocking from the handler’s perspective)
pub fn terminal_write(tx: std::sync::mpsc::Sender<Vec<u8>>, data: Vec<u8>) {
    let _ = tx.send(data); // log/handle as appropriate
}

// Worker thread: owns the blocking writer
fn writer_thread(rx: std::sync::mpsc::Receiver<Vec<u8>>, mut writer: impl std::io::Write + Send) {
    while let Ok(bytes) = rx.recv() {
        let _ = writer.write_all(&bytes); // blocking is isolated here
    }
    // sender dropped => thread ends
}
```

This standard targets responsiveness (no stalls), thread safety (no lock/I/O coupling), and correctness (no stale cleanup).