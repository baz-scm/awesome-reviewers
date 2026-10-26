---
title: Avoid blocking in concurrency
description: 'Keep critical threads and shared state responsive: do not perform potentially
  blocking operations while holding locks or on sync IPC/UI threads. Instead, (1)
  narrow lock scope to handle lookup/cloning, (2) move blocking IO into dedicated
  per-entity worker threads fed by channels, and (3) prevent lifecycle/race cleanup
  with generation/versioning.'
repository: cline/cline#v7
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70865
---

Keep critical threads and shared state responsive: do not perform potentially blocking operations while holding locks or on sync IPC/UI threads. Instead, (1) narrow lock scope to handle lookup/cloning, (2) move blocking IO into dedicated per-entity worker threads fed by channels, and (3) prevent lifecycle/race cleanup with generation/versioning.

Apply:
- Lock scope: take the global/map lock briefly, copy the per-session handle, then release before `write_all`, `wait`, or other blocking calls.
- Worker thread + queue: for each session, route writes through a dedicated writer thread so producers only enqueue.
- Lifecycle correctness: when removing/updating sessions from background threads, guard against stale work using a generation/id check.
- Timeouts/probes: if a probe must run near a UI/close handler, offload it and choose a documented “cheaper failure mode” for ambiguous outcomes.

Example pattern (write isolation + minimal lock hold):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex, mpsc}, thread};

struct Session { tx: mpsc::Sender<Vec<u8>> }
type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_session(sessions: Sessions, id: String, mut writer: impl std::io::Write + Send + 'static) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            // blocking write is isolated in worker thread
            let _ = writer.write_all(&bytes);
        }
    });
    sessions.lock().unwrap().insert(id, Session { tx });
}

fn terminal_write(sessions: &Sessions, id: &str, data: Vec<u8>) {
    // global lock only long enough to get the per-session sender
    let tx = sessions.lock().unwrap().get(id).map(|s| s.tx.clone());
    if let Some(tx) = tx { let _ = tx.send(data); }
}
```

This prevents a blocked IO call from stalling IPC command handling or the UI thread, and it reduces the risk of races during session creation/cleanup.