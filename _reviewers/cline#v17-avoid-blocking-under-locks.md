---
title: Avoid Blocking Under Locks
description: When shared state is protected by a lock, ensure **no potentially blocking
  operation** happens while holding that lock or while on a latency-sensitive thread
  (IPC/UI). Instead, (1) hold the shared lock briefly to clone/lookup handles, (2)
  move blocking IO/writes to a dedicated worker, and (3) make cleanup ownership explicit
  to avoid races.
repository: cline/cline#v17
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70883
---

When shared state is protected by a lock, ensure **no potentially blocking operation** happens while holding that lock or while on a latency-sensitive thread (IPC/UI). Instead, (1) hold the shared lock briefly to clone/lookup handles, (2) move blocking IO/writes to a dedicated worker, and (3) make cleanup ownership explicit to avoid races.

Apply this rule by:
- **Lock scope:** Acquire the global/shared lock only long enough to clone a handle or get a pointer to per-session state; release it before `read/write/wait`.
- **IO offload:** Use a per-session writer thread (or async task) fed by an `mpsc` channel so commands only enqueue data.
- **Non-stale cleanup:** If multiple threads can race to remove/replace entries in a map, add **generation/ownership** so cleanup only removes what it still owns.
- **Timeouted probes:** If you must do a blocking probe (e.g., DBus), run it off the caller thread and apply a timeout; document the safe bias for ambiguous outcomes.

Minimal pattern (writer thread + short lock):

```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, thread};
use std::io::Write;
use std::sync::mpsc;

struct Session {
    tx: mpsc::Sender<Vec<u8>>,
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn terminal_write(sessions: Sessions, id: &str, data: &str) -> Result<(), String> {
    // Hold the lock briefly only to get the sender.
    let tx = {
        let mut map = sessions.lock().unwrap();
        map.get(id)
            .map(|s| s.tx.clone())
            .ok_or_else(|| "unknown session".to_string())?
    };
    // Blocking write_all happens elsewhere (writer thread), not here.
    tx.send(data.as_bytes().to_vec()).map_err(|_| "writer stopped".to_string())?;
    Ok(())
}

fn start_session(sessions: Sessions, id: String, mut writer: Box<dyn Write + Send>) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    // Spawn dedicated blocking writer.
    thread::spawn(move || {
        while let Ok(bytes) = rx.recv() {
            let _ = writer.write_all(&bytes); // blocking is OK here
        }
        // Dropping rx ends the writer thread.
    });

    let mut map = sessions.lock().unwrap();
    map.insert(id, Session { tx });
}
```

Also consider generation/ownership when removing sessions from shared maps, so a reader thread can’t delete a newer session that reused the same id.