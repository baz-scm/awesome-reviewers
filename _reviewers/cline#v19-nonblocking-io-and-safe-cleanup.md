---
title: Nonblocking IO and Safe Cleanup
description: When adding concurrency, ensure (1) critical threads aren’t stalled by
  blocking IO, (2) locks aren’t held across blocking calls, and (3) session cleanup/removal
  is race-safe.
repository: cline/cline#v19
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70885
---

When adding concurrency, ensure (1) critical threads aren’t stalled by blocking IO, (2) locks aren’t held across blocking calls, and (3) session cleanup/removal is race-safe.

Apply this in practice:
- Minimize lock scope: hold the shared mutex only long enough to look up/clone a handle, then release it before calling blocking functions (e.g., `write_all`, waits, long reads).
- Use worker/queue patterns for per-resource serialized IO: if an operation can block, route it through a dedicated worker thread (or async task) fed by a channel, so command handlers/UI/event-loop threads only enqueue.
- Make teardown/removal robust against races: when multiple threads can observe and act on a session/map entry, guard removal with an ownership check (e.g., generation/version) so an older worker can’t remove a newer session that reused the same key.

Illustrative pattern:

```rust
use std::{collections::HashMap, sync::{Arc, Mutex, mpsc}, thread};

#[derive(Clone)]
struct Session {
  tx: mpsc::Sender<Vec<u8>>,
  generation: u64,
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn writer_thread(mut rx: mpsc::Receiver<Vec<u8>> /*, mut writer: impl Write */) {
  while let Ok(bytes) = rx.recv() {
    // Blocking write happens here, not on caller/UI thread.
    // writer.write_all(&bytes)?;
  }
}

fn terminal_write(sessions: &Sessions, id: &str, bytes: Vec<u8>) {
  // Lock only to get the sender; drop lock before blocking/long work.
  let tx = {
    let map = sessions.lock().unwrap();
    map.get(id).map(|s| s.tx.clone()).expect("no session")
  };
  let _ = tx.send(bytes); // enqueue only
}

fn cleanup_if_current(sessions: &Sessions, id: &str, expected_generation: u64) {
  let mut map = sessions.lock().unwrap();
  if map.get(id).map(|s| s.generation) == Some(expected_generation) {
    map.remove(id);
  }
}
```

Use a similar approach for any “probe” or “property read” that might stall: run it off the UI/event thread and apply a timeout so the caller can decide without blocking indefinitely.