---
title: Avoid blocking locks
description: 'Concurrency standard: never let blocking I/O (or potentially slow operations)
  run while holding a shared lock, and never stall latency-sensitive threads (e.g.,
  UI/main). Instead, narrow lock scope to fast handle access, delegate blocking work
  to a per-resource worker (thread/task) fed by a queue/channel, and make cleanup
  race-safe using ownership/generation...'
repository: cline/cline#v14
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70876
---

Concurrency standard: never let blocking I/O (or potentially slow operations) run while holding a shared lock, and never stall latency-sensitive threads (e.g., UI/main). Instead, narrow lock scope to fast handle access, delegate blocking work to a per-resource worker (thread/task) fed by a queue/channel, and make cleanup race-safe using ownership/generation checks. When you use timeouts, decide and document what the timeout means (especially for ambiguous “host missing vs slow responder” cases).

How to apply:
- Lock scope rule: hold shared/global locks only long enough to look up/clone a handle; release before any `write_all`, DBus call, waiting, or other blocking operation.
- Per-resource worker: for each session/resource, run a dedicated writer/worker loop that performs blocking operations; public APIs only enqueue work.
- Race-safe cleanup: background threads must remove/close state only if it still matches their creation token (generation/id), otherwise skip.
- Timeouts for slow probes: run the slow probe off the main thread and use a bounded wait; document the bias/fallback behavior.

Example pattern (writer thread + narrow lock + generation-safe cleanup):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, sync::mpsc};

struct Session {
    tx: mpsc::Sender<Vec<u8>>,
    gen: u64,
}

struct State { sessions: Arc<Mutex<HashMap<String, Session>>> }

fn terminal_write(state: &State, id: &str, data: Vec<u8>) {
    // 1) Hold the lock only to grab the per-session sender.
    let tx = {
        let mut map = state.sessions.lock().unwrap();
        let sess = map.get(id).expect("missing session");
        sess.tx.clone()
    }; // lock released here

    // 2) Enqueue; actual blocking write happens in the worker.
    let _ = tx.send(data);
}

fn spawn_reader_cleanup(state: State, id: String, my_gen: u64) {
    std::thread::spawn(move || {
        // ... read loop ...

        // 3) Cleanup is conditional on ownership/gen.
        let mut map = state.sessions.lock().unwrap();
        if map.get(&id).map(|s| s.gen) == Some(my_gen) {
            map.remove(&id);
        }
    });
}
```