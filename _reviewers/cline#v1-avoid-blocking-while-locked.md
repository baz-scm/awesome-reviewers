---
title: Avoid Blocking While Locked
description: Keep concurrency predictable by ensuring shared locks are held only for
  fast state access, while blocking I/O and slow operations run elsewhere; also make
  session cleanup/races ownership-aware.
repository: cline/cline#v1
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 70862
---

Keep concurrency predictable by ensuring shared locks are held only for fast state access, while blocking I/O and slow operations run elsewhere; also make session cleanup/races ownership-aware.

Rules:
1) Never hold a global/shared lock across blocking I/O (e.g., write_all on a PTY, network calls, DBus reads). Acquire the lock to find/clone lightweight handles, then release before the blocking work.
2) If a command path must stay responsive (IPC handlers, UI callbacks), offload blocking I/O to a dedicated per-resource worker thread. Feed it via an mpsc channel; the command path should only enqueue.
3) Make lifecycle replacement/removal race-safe: when a session can be replaced, remove only if the entry still belongs to the same generation/owner; otherwise another thread might delete the wrong session.
4) For slow external probes that must not stall a critical thread (UI main thread), run them on a background thread and enforce a short timeout; on timeout, treat as failure but let the background task finish.

Sketch:
```rust
// 1) Lock briefly, then enqueue (no blocking write under the sessions lock).
let tx = {
    let mut sessions = state.sessions.lock().unwrap_or_else(|e| e.into_inner());
    sessions.get(&id).ok_or("missing")?.tx.clone()
};
// 2) Enqueue; return quickly.
tx.send(data).map_err(|_| "writer stopped")?;

// Worker owns the blocking I/O.
std::thread::spawn(move || {
    while let Ok(bytes) = rx.recv() {
        // blocking I/O happens here, not on the IPC/UI thread
        let _ = writer.write_all(&bytes);
    }
});

// 3) Ownership-aware cleanup (generation/owner) when reader thread ends.
let generation = my_generation;
state.sessions.lock().unwrap().remove_if(|entry| entry.generation == generation);
```

Applying this standard prevents stalls (responsive IPC/UI), avoids lock contention deadlocks, and eliminates subtle races during session replacement and shutdown.