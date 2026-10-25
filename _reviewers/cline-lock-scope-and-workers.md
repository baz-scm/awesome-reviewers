---
title: Lock Scope And Workers
description: When concurrency touches shared state, ensure (a) mutexes don’t guard
  blocking I/O, (b) slow/blocking operations run on dedicated worker threads, (c)
  state cleanup is race-safe, and (d) any external probe has a timeout and non-fatal
  fallback.
repository: ClInE/cLiNe
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70838
---

When concurrency touches shared state, ensure (a) mutexes don’t guard blocking I/O, (b) slow/blocking operations run on dedicated worker threads, (c) state cleanup is race-safe, and (d) any external probe has a timeout and non-fatal fallback.

Practical rules
1) Don’t hold locks across blocking calls
- If you need to write to a PTY/socket/file, avoid doing `write_all(...)` while holding the shared sessions mutex.
- Instead: lock briefly to fetch/clone the per-session handle, then release the lock before the blocking operation.

2) Offload long/contended I/O to worker threads
- For per-session streaming, create a writer worker per session.
- `terminal_write` (or similar request handlers) should only enqueue work (e.g., via `mpsc`), so the command/IPC/UI thread stays responsive.
- When the session ends, drop the sender so the worker exits naturally.

3) Make cleanup/removal race-safe
- If background threads can outlive (or overlap with) state replacement, ensure a stale thread can’t remove the wrong entry.
- Use a generation/version token (or equivalent) so the reader/worker removes only if the current entry matches its own generation.

4) Never block critical threads on external probes; use timeouts
- For UI/main-thread-triggered checks (tray availability, bus queries, DNS, etc.), run the blocking probe on a separate thread/task.
- Enforce a bounded timeout; on timeout, choose the safer fallback behavior rather than stalling.

5) Guard lifecycle concurrency at the app level
- If duplicate process startup would create competing side effects (tray/sidecar creation, multiple windows, etc.), enforce single-instance behavior so only one instance performs setup.

Illustrative pattern (writer worker + enqueue)
```rust
use std::{sync::{Arc, Mutex, mpsc}, thread};

struct Session { tx: mpsc::Sender<Vec<u8>> }

fn start_session(shared: Arc<Mutex<std::collections::HashMap<String, Session>>>, id: String) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();

    // Writer worker: only this thread performs blocking writes.
    thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            // blocking I/O here, not under shared locks
            // pty_writer.write_all(&bytes).ok();
        }
        // tx dropped => worker ends
    });

    shared.lock().unwrap().insert(id, Session { tx });
}

fn terminal_write(shared: &Arc<Mutex<std::collections::HashMap<String, Session>>>, id: &str, data: Vec<u8>) {
    // Lock only long enough to grab the sender.
    let tx = { shared.lock().unwrap().get(id).unwrap().tx.clone() };
    let _ = tx.send(data); // enqueue; never block here
}
```
Use this standard to prevent UI/IPC stalls, avoid lock-induced deadlocks/perf cliffs, and eliminate stale-thread state races.