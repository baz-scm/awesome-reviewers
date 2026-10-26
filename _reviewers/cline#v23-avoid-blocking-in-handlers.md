---
title: Avoid blocking in handlers
description: 'When code runs on a “hot” thread (IPC/command handler, GUI main thread,
  or other synchronous request path), never perform potentially-blocking I/O while
  holding broad locks. Instead:'
repository: cline/cline#v23
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70889
---

When code runs on a “hot” thread (IPC/command handler, GUI main thread, or other synchronous request path), never perform potentially-blocking I/O while holding broad locks. Instead:

- Keep lock scope minimal: lock only to grab a handle (e.g., sender/clone), then release before any blocking operation.
- Offload blocking work to dedicated worker threads (often one per session/task) and communicate via channels/queues.
- Use lifecycle guards for shared maps: on cleanup, ensure you remove/update only the state that belongs to the current session (IDs/generations), so concurrent reader/writer threads can’t race and delete newer state.
- If you must probe something during UI close/critical sections, run the probe in the background and enforce a timeout; if it overruns, let it finish without blocking the UI thread.

Example pattern (queue + worker instead of direct blocking write):

```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, thread};
use std::sync::mpsc;

type Sessions = Arc<Mutex<HashMap<String, mpsc::UnboundedSender<Vec<u8>>>>>;

fn start_session(sessions: Sessions, id: String) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();

    // Store only the sender under the shared lock, then release.
    {
        let mut map = sessions.lock().unwrap();
        map.insert(id.clone(), tx);
    }

    // Worker thread performs blocking PTY write.
    thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            // blocking write_all(bytes) to PTY goes here
        }
        // When sender is dropped (kill/exit), loop ends.
    });
}

fn terminal_write(sessions: Sessions, id: &str, data: Vec<u8>) {
    let sender = {
        let map = sessions.lock().unwrap();
        map.get(id).cloned().ok_or_else(|| "missing session")?
    }; // lock released before enqueue

    let _ = sender.send(data);
}
```

Apply the same idea to lifecycle: when a reader thread exits, delete only if the session is still current (e.g., check generation/ID), and avoid stalling cleanup paths that other threads rely on.