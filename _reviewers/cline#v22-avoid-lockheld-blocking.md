---
title: Avoid Lockheld Blocking
description: Do not let potentially blocking operations (I/O, waits, long computations)
  run while holding shared locks or on latency-sensitive threads (UI/main/IPC handler
  threads). Instead, minimize lock scope and/or delegate blocking work to per-resource
  worker threads.
repository: cline/cline#v22
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70886
---

Do not let potentially blocking operations (I/O, waits, long computations) run while holding shared locks or on latency-sensitive threads (UI/main/IPC handler threads). Instead, minimize lock scope and/or delegate blocking work to per-resource worker threads.

Apply this standard:
- Keep mutex guards short-lived: never call `read`, `write_all`, `wait`, or other blocking functions while you hold a lock.
- For synchronous request handlers that must remain responsive, route blocking I/O through a dedicated worker per session/resource:
  - the handler enqueues work on a channel and returns quickly
  - the worker performs the actual blocking write/read
  - shutdown should stop the worker by dropping the sender / closing the session
- For UI/main-thread callbacks, offload probes to background threads and decide using a bounded timeout; if you must choose a direction under ambiguity, document it and test it.
- For cleanup of shared registries/maps under concurrency, make removal safe against stale entries (e.g., generation/ownership checks), so late worker shutdown can’t delete a newer session.

Example pattern (writer thread + enqueue):
```rust
use std::{sync::{Arc, Mutex, mpsc}, thread};

struct Session {
    tx: mpsc::Sender<Vec<u8>>, // enqueue writes
}

fn start_writer_thread() -> mpsc::Sender<Vec<u8>> {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    thread::spawn(move || {
        // Do blocking PTY writes here, not in the IPC/UI handler.
        while let Ok(bytes) = rx.recv() {
            // pty_write_all(&bytes); // blocking allowed
        }
    });
    tx
}

fn terminal_write(sessions: &Arc<Mutex<std::collections::HashMap<String, Session>>>, id: &str, data: Vec<u8>) {
    // Lock only long enough to clone the sender.
    let tx = {
        let map = sessions.lock().unwrap();
        map.get(id).expect("missing session").tx.clone()
    };
    // No lock held; enqueue only.
    let _ = tx.send(data);
}
```