---
title: Avoid Blocking Under Locks
description: When implementing concurrency for IPC/UI-triggered actions, ensure shared
  locks and latency-sensitive threads are never blocked by long-running or blocking
  operations.
repository: cline/cline#v16
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70882
---

When implementing concurrency for IPC/UI-triggered actions, ensure shared locks and latency-sensitive threads are never blocked by long-running or blocking operations.

**Standards**
1. **Never do potentially-blocking I/O while holding a broad/shared lock.** Keep lock scope small; copy/clone handles under the lock, then release it before `write_all`, `read`, waits, or channel sends that may block.
2. **For per-session I/O, prefer a worker thread + channel.** The request path should only enqueue work; a dedicated thread performs the blocking writes/reads.
3. **Make background cleanup race-safe.** If sessions can be replaced, use an ownership check (e.g., generation/token) so the worker removes state only if it still owns it.
4. **Use timeouts for off-thread probes triggered by main/UI handlers.** Spawn the probe, wait with `recv_timeout` (or equivalent), and on timeout preserve the pre-existing safe behavior.

**Example (pattern)**
```rust
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::sync::mpsc::{self, Sender};
use std::thread;

struct Session { tx: Sender<Vec<u8>>, generation: u64 }
type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_session(id: String, sessions: Sessions) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    let generation = 1; // increment/store in real code

    // Spawn worker that owns the blocking writer.
    thread::spawn(move || {
        while let Ok(chunk) = rx.recv() {
            // blocking write to PTY/sink happens here (no global locks held)
            // pty_writer.write_all(&chunk).ok();
        }
    });

    sessions.lock().unwrap().insert(id, Session { tx, generation });
}

fn terminal_write(sessions: Sessions, id: &str, data: Vec<u8>) {
    // Lock briefly to fetch the per-session sender, then release.
    let tx = {
        let guard = sessions.lock().unwrap();
        guard.get(id).map(|s| s.tx.clone()).expect("missing session")
    };
    // Enqueue; request thread should not block on the actual I/O.
    let _ = tx.send(data);
}
```

Apply this consistently to avoid IPC thread stalls, UI freezes, and state corruption from background threads that outlive or race with session replacement.