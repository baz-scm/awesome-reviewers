---
title: Avoid blocking under locks
description: 'When concurrency involves shared maps/state plus background threads,
  ensure: (1) you don’t hold mutexes while doing blocking I/O/work, (2) async cleanup
  can’t overwrite newer state, and (3) lock ordering is explicit.'
repository: cline/cline#v25
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70891
---

When concurrency involves shared maps/state plus background threads, ensure: (1) you don’t hold mutexes while doing blocking I/O/work, (2) async cleanup can’t overwrite newer state, and (3) lock ordering is explicit.

**How to apply**
1. **Keep mutex scope tiny**: lock, copy/clone the needed handle(s), then release the lock before any potentially blocking call.
2. **Decouple blocking I/O**: if writes/reads can block, move them to a per-resource worker thread; the RPC/API thread should only enqueue.
3. **Prevent stale workers from mutating successors**: when sessions/children can be replaced, tag entries with an identity/generation and only remove/update if the worker still owns the same generation/child id.
4. **State your lock order** when multiple mutexes exist: document acquisition order and avoid reverse order elsewhere.

**Illustrative pattern**
```rust
use std::{collections::HashMap, sync::{Arc, Mutex}, sync::mpsc};

struct WriterHandle { tx: mpsc::Sender<Vec<u8>> }
type Sessions = Arc<Mutex<HashMap<String, WriterHandle>>>;

// RPC thread: quick lock, enqueue only (no blocking I/O under the lock)
fn terminal_write(sessions: &Sessions, id: &str, data: &[u8]) -> Result<(), String> {
    let tx = {
        let mut map = sessions.lock().map_err(|_| "poisoned")?;
        map.get(id).ok_or("missing session")?.tx.clone()
    }; // lock released here
    tx.send(data.to_vec()).map_err(|_| "writer stopped")
}

// Worker thread: owns the blocking write
fn spawn_writer_thread(sessions: &Sessions, id: String) {
    let (tx, rx) = mpsc::channel::<Vec<u8>>();
    sessions.lock().unwrap().insert(id.clone(), WriterHandle { tx });
    std::thread::spawn(move || {
        let mut writer = /* open PTY writer */ unimplemented!();
        for chunk in rx { let _ = writer.write_all(&chunk); }
        // worker exit: writer stopped
    });
}
```

Also, for any cleanup like “remove from map” or “clear endpoint”, add an ownership check (generation/child id) so late events from replaced workers can’t wipe newer state.