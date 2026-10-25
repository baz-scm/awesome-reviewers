---
title: Avoid lock-held blocking
description: 'When code performs concurrent I/O and lifecycle management, apply these
  rules:


  1) Don’t hold broad/shared locks across blocking work

  - Pattern: acquire the shared map/registry lock only long enough to locate/clone
  a per-session handle; immediately release it before calling anything that can block
  (e.g., `write_all`, `wait`, `read`).'
repository: CLINE/CLINE
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70837
---

When code performs concurrent I/O and lifecycle management, apply these rules:

1) Don’t hold broad/shared locks across blocking work
- Pattern: acquire the shared map/registry lock only long enough to locate/clone a per-session handle; immediately release it before calling anything that can block (e.g., `write_all`, `wait`, `read`).
- If blocking is possible, treat it as a “don’t hold locks” zone.

2) Offload blocking I/O to dedicated per-resource workers
- Use a per-session worker thread (or async task) that owns the blocking writer/reader.
- Enqueue from command/IPC handlers via a channel; the IPC handler should do non-blocking work (enqueue + return).

Example pattern (writer thread + enqueue):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, thread};
use std::sync::mpsc::{self, Sender};

type Sessions = Arc<Mutex<HashMap<String, Sender<Vec<u8>>>>>;

fn spawn_writer(id: String, writer: impl std::io::Write + Send + 'static, sessions: Sessions) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    sessions.lock().unwrap().insert(id, tx);

    thread::spawn(move || {
        let mut writer = writer;
        for bytes in rx {
            // blocks, but no global lock is held here
            let _ = writer.write_all(&bytes);
        }
    });
}

fn terminal_write(sessions: &Sessions, id: &str, data: Vec<u8>) -> Result<(), String> {
    let tx = sessions.lock().unwrap()
        .get(id)
        .cloned()
        .ok_or_else(|| "session missing".to_string())?;
    // no locks held during send; worker performs blocking writes
    tx.send(data).map_err(|_| "session ended".to_string())
}
```

3) Prevent stale threads from overwriting newer state
- If a resource can be replaced/retried (session/tab, sidecar child, etc.), use an identity guard (generation number, session id+generation, or child pid) so late cleanup/removal only acts if it still owns the current resource.
- Never let “EOF on an old thread” clear state for a newer instance.

4) Make lock ordering explicit
- Document and enforce a single global lock order when multiple mutexes can be held together (e.g., `process` before `ws_endpoint`, never reverse). This prevents deadlocks.

Adopting these four rules will eliminate common issues seen in the discussed code: IPC stalls from lock-held blocking I/O, deadlocks from inconsistent lock ordering, and racey state corruption from late cleanup during replacement.