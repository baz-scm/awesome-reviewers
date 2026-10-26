---
title: Avoid Blocking Under Locks
description: When implementing multithreaded stateful services, ensure shared locks
  are never held across potentially blocking operations, and make cleanup/state updates
  race-safe.
repository: cline/cline#v5
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70864
---

When implementing multithreaded stateful services, ensure shared locks are never held across potentially blocking operations, and make cleanup/state updates race-safe.

Apply these rules:
1) Keep lock scope minimal
- Acquire shared maps/locks briefly to fetch/clone handles.
- Release before calling anything that can block (e.g., `write_all`, IPC sends that might block, filesystem/network IO).

2) Decouple blocking IO from command threads
- Use a per-session worker (thread/task) that owns the blocking writer, fed by an unbounded/buffered channel/queue.
- The API/IPC entrypoint only enqueues data, staying responsive.

3) Make concurrent cleanup deterministic
- If background threads can still run while you remove state on exit/kill, guard removal with a generation/version so a late thread can’t delete a newer session entry.

4) For external probes/timeouts: never block the caller thread
- Run the probe off-thread and use a timeout.
- Choose the timeout’s “wrong-direction” based on which outcome is safer for currently running work, and document that bias.

Example pattern (writer worker + nonblocking enqueue):

```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, io::Write};
use std::sync::mpsc::{self, Sender};

struct Session {
    writer_tx: Sender<Vec<u8>>,
    // generation, etc.
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn spawn_writer_thread(mut writer: impl Write + Send + 'static) -> Sender<Vec<u8>> {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    std::thread::spawn(move || {
        for chunk in rx {
            // Blocking write happens only in this worker.
            let _ = writer.write_all(&chunk);
        }
    });
    tx
}

fn terminal_write(sessions: &Sessions, id: &str, data: Vec<u8>) {
    // Hold the sessions lock only long enough to fetch the sender.
    let tx = {
        let mut map = sessions.lock().unwrap();
        map.get(id).unwrap().writer_tx.clone()
    };
    // Enqueue only; enqueue should be fast.
    let _ = tx.send(data);
}
```

If you also need safe removal under concurrent reader/kill/exit, add a generation/version check before deleting the session entry.