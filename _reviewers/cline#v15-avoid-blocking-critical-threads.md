---
title: Avoid blocking critical threads
description: 'When implementing concurrency, ensure that potentially blocking operations
  (e.g., PTY writes, IPC sends/receives, D-Bus calls) never run while holding a shared
  mutex or on an event-loop/critical thread. Instead:'
repository: cline/cline#v15
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70877
---

When implementing concurrency, ensure that potentially blocking operations (e.g., PTY writes, IPC sends/receives, D-Bus calls) never run while holding a shared mutex or on an event-loop/critical thread. Instead:

- Hold locks briefly: use the lock only for quick lookups/clones/enqueues, then release it before any blocking call.
- Offload blocking I/O: give each long-lived resource (like a terminal session) its own worker thread that performs the blocking write, and let the main command path only enqueue work (e.g., via an mpsc channel).
- Protect event loops: if you must probe something that can stall, run it in a worker and enforce a timeout so the UI thread stays responsive.
- Initialize concurrency gates first: if duplicate-instance/lifecycle gating is required, register it before creating other concurrent components to prevent racey side effects.

Example pattern (short lock + enqueue to a per-session writer thread):

```rust
use std::sync::{Arc, Mutex, mpsc};
use std::thread;

struct Session {
    tx: mpsc::Sender<Vec<u8>>,
}

type Sessions = Arc<Mutex<std::collections::HashMap<String, Session>>>;

fn spawn_writer_thread(mut writer: impl std::io::Write + Send + 'static) -> mpsc::Sender<Vec<u8>> {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    thread::spawn(move || {
        for bytes in rx {
            // blocking write happens only in this dedicated thread
            let _ = writer.write_all(&bytes);
        }
    });
    tx
}

fn terminal_write(sessions: Sessions, id: &str, data: Vec<u8>) -> Result<(), String> {
    let tx = {
        let mut guard = sessions.lock().map_err(|_| "lock poisoned")?;
        guard.get(id).ok_or("missing session")?.tx.clone()
    }; // lock released before blocking work

    tx.send(data).map_err(|_| "writer thread ended")
}
```

Apply the same principle to UI/GTK/IPC “probe” logic: run the potentially slow call in a worker thread and decide using `recv_timeout`, so the UI thread never blocks.