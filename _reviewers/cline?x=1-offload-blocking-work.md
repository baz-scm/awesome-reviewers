---
title: Offload Blocking Work
description: Blocking I/O and long waits must not run on threads that handle synchronous
  IPC commands or UI/GTK callbacks. Use worker threads plus message passing, keep
  locks out of blocking paths, and make teardown/removal race-safe.
repository: cline/cline?x=1
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70861
---

Blocking I/O and long waits must not run on threads that handle synchronous IPC commands or UI/GTK callbacks. Use worker threads plus message passing, keep locks out of blocking paths, and make teardown/removal race-safe.

Apply this as a checklist:
- Keep IPC/UI threads responsive:
  - If you must perform potentially blocking operations (e.g., PTY writes, DBus/property reads), move them to a dedicated worker.
  - For UI callbacks, run the probe asynchronously and enforce a short timeout; if it overruns, let it finish without blocking the callback.
- Minimize lock scope:
  - Never hold a global/session-map lock while performing `write_all`, waiting, or other blocking operations.
  - Prefer: lock briefly to fetch/clone a handle, then release before blocking.
- Make async teardown race-safe:
  - When sessions can be replaced/reinserted, async tasks must not remove the wrong entry.
  - Use a generation/version token and only remove if the generation still matches.

Example pattern (writer worker + enqueue):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}};
use std::sync::mpsc;

struct Session {
    tx: mpsc::Sender<Vec<u8>>,
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_session(id: String, sessions: Sessions, writer: impl std::io::Write + Send + 'static) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();

    // Worker thread owns the blocking writer.
    std::thread::spawn(move || {
        let mut w = writer;
        for data in rx {
            // Blocking write happens only here.
            let _ = w.write_all(&data);
        }
        // Sender drop ends the worker.
    });

    // Lock briefly to register the session.
    sessions.lock().unwrap().insert(id, Session { tx });
}

fn terminal_write(sessions: Sessions, id: &str, data: Vec<u8>) {
    // Lock only to clone/enqueue; do not block while holding the lock.
    let tx = {
        let map = sessions.lock().unwrap();
        map.get(id).map(|s| s.tx.clone())
    };
    if let Some(tx) = tx {
        let _ = tx.send(data); // enqueue only
    }
}
```

Use generation/version tokens for safe removal when async readers/writers can outlive a replacement. This prevents races like “remove the new session because the old one finished.”