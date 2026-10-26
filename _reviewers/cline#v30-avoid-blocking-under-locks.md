---
title: Avoid Blocking Under Locks
description: 'When adding concurrency, ensure critical threads aren’t blocked and
  shared locks aren’t held across blocking operations.


  Practical rules:

  1) Don’t hold a global mutex while doing blocking IO/IPC.'
repository: cline/cline#v30
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70894
---

When adding concurrency, ensure critical threads aren’t blocked and shared locks aren’t held across blocking operations.

Practical rules:
1) Don’t hold a global mutex while doing blocking IO/IPC.
   - If you need to write, take the lock only long enough to obtain/copy the handle, then release before any `write_all`/blocking call.
2) If writes/IO can block, decouple them from request handling.
   - Create a per-resource worker thread and feed it via a channel; the public method only enqueues.
3) Make lifecycle/races explicit.
   - On shutdown/replace, ensure the worker exits when the sender is dropped, and use a generation/id check when removing shared map entries to avoid stale removals.
4) For UI/critical-thread work, always offload and bound latency.
   - Run blocking probes in a background thread and use a timeout; document the behavior under timeout/ambiguity.

Example pattern (enqueue-only write path):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex, mpsc}, thread};

type Sessions = Arc<Mutex<HashMap<String, mpsc::Sender<Vec<u8>>>> >;

fn start_session(sessions: Sessions, id: String) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    sessions.lock().unwrap().insert(id.clone(), tx);

    thread::spawn(move || {
        // worker owns the blocking writer
        let mut writer = /* obtain writer */;
        while let Ok(bytes) = rx.recv() {
            // blocking write is safe here; no shared lock is held
            let _ = writer.write_all(&bytes);
        }
        // drop rx => thread ends
    });
}

fn terminal_write(sessions: Sessions, id: &str, data: Vec<u8>) {
    // lock only to grab the sender handle; then enqueue
    let tx = sessions.lock().unwrap().get(id).cloned().ok_or(()).unwrap();
    tx.send(data).ok();
}
```

Apply the same idea to probes/time-based decisions: never let a GTK/UI thread or an IPC handler wait indefinitely—move blocking work to background threads and decide with a bounded timeout.