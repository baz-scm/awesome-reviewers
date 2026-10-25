---
title: Avoid blocking under locks
description: 'When writing concurrent code, keep caller threads (IPC/UI/request handlers)
  responsive and prevent lifecycle races.


  Apply these rules:

  1) Never perform blocking IO while holding a broad/global lock. Lock briefly to
  fetch/clone the needed state, then release.'
repository: CLINE/cline
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70839
---

When writing concurrent code, keep caller threads (IPC/UI/request handlers) responsive and prevent lifecycle races.

Apply these rules:
1) Never perform blocking IO while holding a broad/global lock. Lock briefly to fetch/clone the needed state, then release.
2) If an operation may block (e.g., PTY writes), move it to a dedicated worker owned by the resource (session). The public API should only enqueue work.
3) If entries can be replaced (e.g., same ID re-used), guard cleanup/removal with a stable identity (generation/token) so an old thread can’t delete the new one.
4) For timeouts, define what the timeout “means” and bias toward the safer behavior; document the reasoning.

Example pattern (session-owned writer thread):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex, mpsc}, thread};

struct Session { tx: mpsc::Sender<Vec<u8>>, generation: u64 }
struct State { sessions: Arc<Mutex<HashMap<String, Session>>>, next_gen: u64 }

fn start_session(state: &mut State, id: String) -> u64 {
    state.next_gen += 1;
    let gen = state.next_gen;

    // Worker owns the potentially-blocking writer.
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            // write_all(...) can block; it must not be on the caller thread.
            let _ = bytes; // writer.write_all(&bytes);
        }
    });

    state.sessions.lock().unwrap().insert(id, Session { tx, generation: gen });
    gen
}

fn terminal_write(state: &State, id: &str, data: Vec<u8>) -> Result<(), String> {
    // Hold the lock only to find the session handle, then enqueue.
    let tx = {
        let map = state.sessions.lock().map_err(|_| "lock poisoned")?;
        map.get(id).ok_or("session missing")?.tx.clone()
    };
    tx.send(data).map_err(|_| "session ended")
}
```

Adopt these practices to reduce stalls, avoid accidental deadlocks, and make cleanup and timeouts predictable under concurrent execution.