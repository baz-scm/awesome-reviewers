---
title: Avoid Blocking Under Locks
description: 'When working with concurrency, ensure the system remains responsive
  and race-safe by following three rules:


  1) Don’t hold shared locks across blocking operations'
repository: cline/cline#v9
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70868
---

When working with concurrency, ensure the system remains responsive and race-safe by following three rules:

1) Don’t hold shared locks across blocking operations
- Keep lock scope small: acquire the sessions/map lock only long enough to fetch/clone a handle, then release it before any `write_all`, `read`, waits, or other potentially blocking calls.
- Prefer per-session synchronization or worker threads for IO so “API/IPC thread” work becomes non-blocking (enqueue only).

2) Isolate blocking or slow work behind timeouts on background threads
- If code runs on a critical thread (UI/GTK/main thread, IPC handler, command thread), move the blocking probe/IO to a worker thread.
- Use explicit timeouts and make the timeout resolution deterministic and documented (i.e., choose the cheaper wrong outcome, and record the reasoning).
- If the probe overruns, let it complete without blocking the caller.

3) Make lifecycle transitions race-safe
- Assume sessions/entries can be replaced while workers are still running.
- Use ownership tokens/generations (or equivalent) so that cleanup/removal only happens if the worker still refers to the current instance.

Practical pattern (writer thread + enqueue-only writes):
```rust
use std::{sync::{Arc, Mutex}, thread};
use std::sync::mpsc;

struct Session {
  tx: mpsc::Sender<Vec<u8>>,
}

fn spawn_writer(mut writer: impl std::io::Write + Send + 'static) -> mpsc::Sender<Vec<u8>> {
  let (tx, rx) = mpsc::channel::<Vec<u8>>();
  thread::spawn(move || {
    for chunk in rx {
      // Blocking write happens only in the worker thread.
      let _ = writer.write_all(&chunk);
    }
    // Dropping rx ends the thread.
  });
  tx
}

fn terminal_write(sessions: &Arc<Mutex<std::collections::HashMap<String, Session>>>, id: &str, data: Vec<u8>) {
  // Lock briefly to clone/lookup the sender, then release the lock.
  let tx = {
    let map = sessions.lock().unwrap();
    map.get(id).unwrap().tx.clone()
  };
  // Enqueue only; never block the caller on IO.
  let _ = tx.send(data);
}
```

Also apply the same thinking to probes/time-bounded checks: background worker + timeout + documented “fail-safe” direction, rather than blocking the caller or leaving behavior ambiguous.