---
title: Avoid blocking under locks
description: 'When concurrency meets I/O and shared state, ensure (1) responsiveness
  and (2) correctness under races:


  - **Do not hold shared locks while performing blocking I/O.** Clone/lookup needed
  handles under the lock, then release the lock before calling `write_all`/waiting/reads.'
repository: cline/cline#v10
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70869
---

When concurrency meets I/O and shared state, ensure (1) responsiveness and (2) correctness under races:

- **Do not hold shared locks while performing blocking I/O.** Clone/lookup needed handles under the lock, then release the lock before calling `write_all`/waiting/reads.
- **Isolate blocking or potentially stalled I/O in a per-resource worker.** Route requests via a channel; request threads only enqueue and return.
- **Prevent stale workers from mutating state after replacement/teardown.** Use **generation/ownership tokens** so only the current worker may remove/update its session entry.
- **If you must probe/await with timeouts, run it off the critical/UI thread and document the safest timeout outcome.**

Example pattern (per-session writer thread + enqueue):

```rust
// Shared map holds session state, but the IPC/request thread only enqueues.
// The writer thread does all blocking write_all.
use std::{collections::HashMap, sync::{Arc, Mutex, mpsc}};

struct Session { tx: mpsc::Sender<Vec<u8>> }
type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn start_writer_worker(id: String, rx: mpsc::Receiver<Vec<u8>>, /* pty writer */ mut writer: impl std::io::Write + Send + 'static) {
    std::thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            // Blocking I/O stays in the worker.
            let _ = writer.write_all(&bytes);
        }
    });
}

fn terminal_write(sessions: Sessions, id: &str, data: &[u8]) {
    // Lock only long enough to get the sender; do not hold it during write.
    let tx = {
        let mut guard = sessions.lock().unwrap();
        guard.get(id).unwrap().tx.clone()
    };
    let _ = tx.send(data.to_vec());
}
```

Also apply a **generation check** when removing/updating shared entries so an old reader doesn’t remove a newer session:

```rust
// Pseudocode: only remove if generations match.
if map.get(&id).is_some_and(|s| s.generation == my_generation) {
    map.remove(&id);
}
```

Adopting these rules prevents (a) head-of-line blocking of request threads and (b) race-driven state corruption during session restarts and shutdown.