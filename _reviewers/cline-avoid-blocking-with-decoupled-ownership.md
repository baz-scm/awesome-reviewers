---
title: Avoid blocking with decoupled ownership
description: 'When concurrency involves shared state and/or synchronous callers (IPC
  handlers, UI main thread), follow these rules:


  1) Keep global locks short

  - Hold the “sessions”/registry lock only long enough to find or clone a per-session
  handle. Release it before any blocking work.'
repository: cline/CLINE
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70839
---

When concurrency involves shared state and/or synchronous callers (IPC handlers, UI main thread), follow these rules:

1) Keep global locks short
- Hold the “sessions”/registry lock only long enough to find or clone a per-session handle. Release it before any blocking work.

2) Decouple blocking IO from critical threads
- If a write/read can block (e.g., PTY IO), move it to a dedicated worker per session and communicate via a channel.
- Pattern: `terminal_write` enqueues data; a per-session writer thread performs the blocking `write_all`.

3) Make lifecycle updates race-safe
- When a background thread may outlive or replace the session entry, only remove/cleanup if the entry still matches that thread’s identity (e.g., use a generation counter or store the exact session handle).

4) Use timeouts for cross-process probing
- If you must probe something from a latency-sensitive thread (UI close handler, sync startup), run the probe in the background and apply a timeout so the caller stays responsive. If ambiguity exists (host present but slow vs. truly absent), document the chosen bias.

Example pattern (writer decoupling + safe cleanup):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex, mpsc}, thread};

struct Session {
    tx: mpsc::Sender<Vec<u8>>,
    generation: u64,
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_session(sessions: Sessions, id: String, generation: u64, writer: impl std::io::Write + Send + 'static) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();

    // Register session (under lock, non-blocking)
    sessions.lock().unwrap().insert(id.clone(), Session { tx, generation });

    // Worker thread performs blocking writes
    thread::spawn(move || {
        let mut w = writer;
        for chunk in rx {
            let _ = w.write_all(&chunk); // blocking, but not on the caller/IPC thread
        }
        // When tx is dropped, loop ends.
    });
}

fn terminal_write(sessions: &Sessions, id: &str, data: &[u8]) {
    // Lock only to clone/enqueue; do NOT block while holding it.
    let tx = {
        let map = sessions.lock().unwrap();
        map.get(id).map(|s| s.tx.clone()).unwrap()
    };
    let _ = tx.send(data.to_vec());
}
```

Adopting this standard prevents common stalls (blocked IO freezing IPC/UI), and prevents subtle race bugs where background threads remove or mutate the wrong session entry after replacement.