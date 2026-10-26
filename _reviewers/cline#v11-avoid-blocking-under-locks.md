---
title: Avoid Blocking Under Locks
description: When shared state is accessed from multiple threads/tasks, ensure that
  blocking or long-running operations never occur while holding a shared/global lock,
  and make session cleanup race-safe.
repository: cline/cline#v11
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70871
---

When shared state is accessed from multiple threads/tasks, ensure that blocking or long-running operations never occur while holding a shared/global lock, and make session cleanup race-safe.

Apply this standard:
- Keep lock scope small: lock the shared map only long enough to get/clone handles (writers/killer/generation), then release the lock before doing any blocking work.
- Offload blocking IO: if a write/read may block (PTY writes, IPC sends, filesystem IO), route it through a dedicated per-session worker thread (or async task) fed by a queue; the request thread should only enqueue.
- Make lifecycle cleanup idempotent: when removing session entries after exit, use a generation/identity token so a late cleanup can’t remove a newer session with the same key.
- Never block the UI/main thread: any probe/operation that might wait should run off-thread with an explicit timeout.

Example pattern (inspired by the terminal session changes):
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, thread};
use tokio::sync::mpsc; // or std::sync::mpsc

struct Session {
  writer_tx: mpsc::UnboundedSender<Vec<u8>>,
  generation: u64,
}

type Sessions = Arc<Mutex<HashMap<String, Session>>>;

fn terminal_write(sessions: &Sessions, id: &str, data: Vec<u8>) -> Result<(), String> {
  let tx = {
    let mut map = sessions.lock().unwrap();
    map.get(id)
      .ok_or("no such session")
      .map(|s| s.writer_tx.clone())?
  }; // lock released here
  tx.send(data).map_err(|_| "writer thread ended".to_string())?;
  Ok(())
}

fn spawn_writer_thread(writer: impl std::io::Write + Send + 'static) -> mpsc::UnboundedSender<Vec<u8>> {
  let (tx, mut rx) = mpsc::unbounded_channel();
  thread::spawn(move || {
    let mut w = writer;
    while let Some(chunk) = rx.recv().await {
      let _ = w.write_all(&chunk); // blocking allowed: not under shared locks
    }
  });
  tx
}

fn cleanup(sessions: &Sessions, id: &str, generation: u64) {
  let mut map = sessions.lock().unwrap();
  if map.get(id).map(|s| s.generation) == Some(generation) {
    map.remove(id);
  }
}
```
This prevents deadlocks/stalls (from blocking while holding locks), keeps IPC/UI responsive, and avoids racey removal of the wrong session.