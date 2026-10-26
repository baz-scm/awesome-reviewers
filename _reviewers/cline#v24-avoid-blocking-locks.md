---
title: Avoid blocking locks
description: When writing concurrent code, ensure that long/blocking work never holds
  shared locks or runs on critical request/UI threads. Use per-resource workers/queues,
  and add lifecycle ownership checks to prevent races during replacement/cleanup.
repository: cline/cline#v24
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70891
---

When writing concurrent code, ensure that long/blocking work never holds shared locks or runs on critical request/UI threads. Use per-resource workers/queues, and add lifecycle ownership checks to prevent races during replacement/cleanup.

Apply this as a team rule:
- Keep lock scope minimal: take the shared lock only long enough to locate/clone a handle; release it before any blocking operation (e.g., `write_all`).
- Decouple IO from request threads: route writes/reads through a per-session (or per-resource) worker thread fed by a channel/queue, so the caller only enqueues.
- Make cleanup race-safe: if entries can be replaced, guard removals with generation/ownership checks so an older worker can’t delete a newer session.
- For UI/event probes with timeouts: offload the probe to a worker thread and document which failure mode the timeout is allowed to prefer (based on which outcome is less damaging).

Sketch pattern (IO decoupling + ownership):
```rust
// Shared map: protect only handle lookup.
type Sessions = Arc<Mutex<HashMap<String, Session>>>;

struct Session {
  generation: u64,
  tx: std::sync::mpsc::Sender<Vec<u8>>,
}

fn terminal_write(sessions: &Sessions, id: &str, data: Vec<u8>) -> Result<(), String> {
  // Hold the lock briefly: clone tx, then drop.
  let tx = {
    let mut map = sessions.lock().unwrap();
    map.get(id).ok_or("missing")?.tx.clone()
  };
  // Blocking/IO happens in the worker, not here.
  tx.send(data).map_err(|_| "worker gone".to_string())
}

// Worker owns the potentially-blocking writer.
fn writer_worker(rx: std::sync::mpsc::Receiver<Vec<u8>>, mut writer: impl std::io::Write) {
  for chunk in rx {
    let _ = writer.write_all(&chunk);
  }
}

// Cleanup guard example: only remove if generation matches.
fn try_remove(sessions: &Sessions, id: &str, expected_gen: u64) {
  let mut map = sessions.lock().unwrap();
  if map.get(id).map(|s| s.generation) == Some(expected_gen) {
    map.remove(id);
  }
}
```

This standard prevents stalls, lock contention, and “wrong session removed” bugs while keeping event/UI threads responsive under load or slow downstream behavior.