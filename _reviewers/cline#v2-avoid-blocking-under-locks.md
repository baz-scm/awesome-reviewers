---
title: Avoid Blocking Under Locks
description: 'When implementing concurrent systems (especially session-like or streaming
  components), enforce these rules:


  1) Don’t hold shared locks across blocking operations'
repository: cline/cline#v2
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70861
---

When implementing concurrent systems (especially session-like or streaming components), enforce these rules:

1) Don’t hold shared locks across blocking operations
- Keep the scope of any global/shared mutex as small as possible.
- Functions exposed to RPC/IPC/GUI threads should not perform `read/recv/write_all/wait` while holding a mutex.

2) Prefer per-entity worker threads/tasks for blocking IO
- If an operation may block (e.g., writing to a PTY), move it to a dedicated worker for that entity.
- Make the public API enqueue-only (fast path). Use a queue/channel to feed the worker.

Example pattern (writer thread + enqueue-only command):
```rust
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::io::Write;

struct Session {
    tx: mpsc::Sender<Vec<u8>>, // enqueue only
}

fn start_session(mut writer: Box<dyn Write + Send>, rx_data: mpsc::Receiver<Vec<u8>>) {
    thread::spawn(move || {
        // Blocking write happens here, not in the caller.
        while let Ok(bytes) = rx_data.recv() {
            let _ = writer.write_all(&bytes);
            let _ = writer.flush();
        }
        // Dropping session sender/receiver ends the worker.
    });
}

fn terminal_write(session: &Session, data: &[u8]) {
    let _ = session.tx.send(data.to_vec());
}
```

3) Make teardown/removal race-safe
- When background threads/readers/writers can outlive a map entry, don’t rely on “remove by id” alone.
- Use a generation/version token so a thread only removes or updates state if it still matches its own generation.

4) For latency-sensitive threads, bound external/IPC work
- If you must probe something that can stall (DBus/IPC/filesystem/network), run it off-thread and use a timeout.
- Document which failure direction is safer when the timeout triggers.

Applying these rules prevents deadlocks, UI/IPC stalls, and “use-after-teardown” races, while keeping responsiveness predictable.