---
title: Avoid blocking locks
description: Keep critical sections short and never perform potentially blocking work
  while holding shared state (mutexes) or on UI/main threads. Instead, isolate blocking
  I/O behind per-resource workers (threads) and communicate via channels; make cleanup/removal
  ownership-safe to avoid races.
repository: cline/cline#v18
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70884
---

Keep critical sections short and never perform potentially blocking work while holding shared state (mutexes) or on UI/main threads. Instead, isolate blocking I/O behind per-resource workers (threads) and communicate via channels; make cleanup/removal ownership-safe to avoid races.

Guidelines:
- Don’t hold a shared/global lock during blocking I/O (e.g., `write_all`, PTY reads/writes, network calls). Acquire only long enough to get a handle, then release.
- Prefer worker-per-resource for blocking operations: a session-owned writer thread that receives queued writes via `mpsc`; the command path only enqueues.
- Make teardown/race-safe: when a background reader exits, remove entries only if it still “owns” the current session (e.g., by using a generation/version token).
- For main-thread responsiveness: offload probes/work with bounded timeouts, and document which outcome is acceptable when the timeout fires.

Example (writer isolation + non-blocking enqueue):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, thread};
use tokio::sync::mpsc; // or std::sync::mpsc depending on your stack

struct Session {
  // ... PTY handles ...
  tx: mpsc::UnboundedSender<Vec<u8>>,
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_writer_thread(/* pty writer */ writer: impl std::io::Write + Send + 'static) -> mpsc::UnboundedSender<Vec<u8>> {
  let (tx, mut rx) = mpsc::unbounded_channel::<Vec<u8>>();
  thread::spawn(move || {
    while let Some(bytes) = rx.blocking_recv() {
      // blocking write happens here, not while holding the sessions lock
      let _ = writer.write_all(&bytes);
    }
  });
  tx
}

fn terminal_write(sessions: &Sessions, id: &str, data: Vec<u8>) {
  // lock briefly to clone the per-session sender, then release before blocking
  let tx = {
    let mut map = sessions.lock().unwrap();
    map.get(id).map(|s| s.tx.clone()).expect("missing session")
  };
  let _ = tx.send(data);
}
```

If you’re tempted to “just lock and write”, treat it as a concurrency smell unless you’ve proven the operation cannot block and you’re not on a main/UI thread.