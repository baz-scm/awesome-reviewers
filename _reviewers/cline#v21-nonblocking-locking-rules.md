---
title: Nonblocking Locking Rules
description: 'When implementing concurrency around shared mutable state:


  1) Don’t hold a shared mutex across blocking work

  - Only lock long enough to look up/clone handles or update small state.'
repository: cline/cline#v21
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70886
---

When implementing concurrency around shared mutable state:

1) Don’t hold a shared mutex across blocking work
- Only lock long enough to look up/clone handles or update small state.
- Release the lock before calling blocking APIs like `write_all`, `recv_timeout` loops, or waiting on threads.

2) Isolate potentially blocked I/O with a per-resource worker
- If a caller may be blocked by the external process (e.g., PTY backpressure), move the blocking write/read to a dedicated worker thread.
- Use message passing so the command/IPC/UI thread only enqueues work.

3) Make lifecycle ownership unambiguous
- If entries in a shared `HashMap` can be replaced (re-spawn, reconnect, tab reuse), add identity metadata (e.g., generation/nonce) so workers only remove/update the map entry they own.

4) For critical-thread operations, always offload + bound
- If a probe/DBus/IPC call could stall (UI close handlers, IPC command handlers), run it off-thread and enforce a timeout.
- Document the chosen default when timeout/ambiguous results occur, biased toward the behavior that recovers more easily.

Example pattern (writer isolation + short lock):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}};
use std::sync::mpsc;
use std::io::Write;

type Sessions = Arc<Mutex<HashMap<String, Session>>>;
struct Session {
    // Protected only for short operations; writer work happens elsewhere.
    writer_tx: mpsc::Sender<Vec<u8>>,
}

fn terminal_write(sessions: Sessions, id: &str, data: &[u8]) -> Result<(), String> {
    // Hold the lock briefly to get the sender, then release.
    let tx = {
        let mut guard = sessions.lock().map_err(|e| e.to_string())?;
        guard.get(id).ok_or_else(|| "missing session".to_string())?
            .writer_tx.clone()
    };
    // Enqueue; do not block in the caller on slow I/O.
    tx.send(data.to_vec()).map_err(|_| "writer thread stopped".to_string())
}

fn start_writer_thread(writer: Box<dyn Write + Send>, rx: mpsc::Receiver<Vec<u8>>) {
    std::thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            // Blocking write happens only here.
            let _ = writer.write_all(&bytes);
        }
    });
}
```
Applying these rules prevents lock contention, avoids stalling IPC/UI threads, and eliminates race-prone state removal/replace bugs.