---
title: Avoid Blocking Under Locks
description: 'Concurrency standard: keep critical sections small, never perform potentially
  blocking work while holding shared locks, and make cleanup race-safe.


  Apply this as follows:'
repository: cline/cline#v3
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70863
---

Concurrency standard: keep critical sections small, never perform potentially blocking work while holding shared locks, and make cleanup race-safe.

Apply this as follows:
- Lock only to access/clone the data needed for the operation; release the lock before calling blocking methods (e.g., write_all, waits, IPC sends that can block).
- Offload blocking IO to a per-entity worker thread (or async task) and communicate with it via a channel. The API/IPC handler should enqueue work and return quickly.
- If entities can be replaced (restart/replace session/tab), cleanup must verify identity (e.g., generation or token) before removing shared state.
- For probes on sensitive threads (UI/close handlers), run the probe off-thread and use a bounded timeout; when ambiguous, document the failure bias.

Example pattern (worker-thread writer with enqueue):

```rust
use std::{collections::HashMap, sync::{Arc, Mutex}};
use std::sync::mpsc;

struct Session {
  tx: mpsc::Sender<Vec<u8>>,
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_session(id: String, writer: impl std::io::Write + Send + 'static, sessions: Sessions) {
  let (tx, rx) = mpsc::channel::<Vec<u8>>();

  // Writer thread owns the blocking writer.
  std::thread::spawn(move || {
    let mut w = writer;
    for chunk in rx {
      // Blocking is OK here; no shared lock held.
      let _ = w.write_all(&chunk);
    }
  });

  sessions.lock().unwrap().insert(id, Session { tx });
}

fn terminal_write(sessions: &Sessions, id: &str, data: Vec<u8>) {
  // Lock briefly, clone/enqueue handle, then unlock.
  let tx = {
    let mut map = sessions.lock().unwrap();
    map.get(id).map(|s| s.tx.clone()).unwrap()
  };
  let _ = tx.send(data); // enqueue only
}
```

If you replace/remove sessions concurrently, guard removal with identity (generation/token) so a newer session isn’t accidentally removed.

For UI-close probes, prefer:
- `thread::spawn` for the probe + `recv_timeout` to keep the close handler responsive.
- Document the chosen timeout bias and rationale (what happens on timeout vs. immediate failure).