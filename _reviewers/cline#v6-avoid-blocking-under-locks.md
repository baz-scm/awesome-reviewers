---
title: Avoid Blocking Under Locks
description: 'When concurrency involves IPC/UI/command threads and shared state, enforce
  these rules:


  1) Don’t hold shared locks across blocking I/O

  - Keep lock scope tiny: acquire lock to grab/clone the needed handle, then release
  the lock before any `write_all`, `read`, waiting, or other blocking work.'
repository: cline/cline#v6
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70864
---

When concurrency involves IPC/UI/command threads and shared state, enforce these rules:

1) Don’t hold shared locks across blocking I/O
- Keep lock scope tiny: acquire lock to grab/clone the needed handle, then release the lock before any `write_all`, `read`, waiting, or other blocking work.

2) Route potentially blocking operations through per-resource workers
- If a write can block (e.g., PTY backpressure), make the command path enqueue-only. Use a per-session worker thread + an `mpsc` channel so callers remain responsive.

3) Make cleanup/removal race-safe
- Late events (reader thread exit, kill, replace) must not remove or overwrite newer sessions. Use a generation/version token so removals only apply if the map still points to the same generation.

4) Keep critical threads responsive with offload + timeout (when needed)
- For operations that might stall (probes, environment checks), run off-thread and apply a timeout; document the risk tradeoff so failure bias is intentional.

Example (enqueue-only writer worker):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, thread};
use std::io::Write;
use std::sync::mpsc;

struct Session { tx: mpsc::Sender<Vec<u8>>, generation: u64 }
type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_writer(mut writer: Box<dyn Write + Send>, sessions: Sessions, id: String, generation: u64) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            // blocking happens only in this worker thread
            let _ = writer.write_all(&bytes);
        }
    });

    sessions.lock().unwrap().insert(id, Session { tx, generation });
}

fn terminal_write(sessions: Sessions, id: &str, data: Vec<u8>) -> Result<(), String> {
    let tx = {
        let map = sessions.lock().unwrap();
        map.get(id).ok_or("no such session")?.tx.clone()
    }; // lock released before blocking/IO
    tx.send(data).map_err(|_| "session ended".to_string())
}
```

Applying these patterns prevents stalled command threads, reduces lock contention, and avoids state corruption from races during session replacement and shutdown.