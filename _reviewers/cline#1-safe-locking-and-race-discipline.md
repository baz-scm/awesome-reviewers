---
title: Safe locking and race discipline
description: Never perform blocking work — I/O, process waits, or network/IPC probes
  — while holding a lock that other threads need for non-blocking access. A thread
  blocked inside `write_all`, a D-Bus call, or `child.wait()` while holding a mutex
  stalls every other caller of that lock, including UI or IPC command threads. Offload
  blocking operations to a dedicated...
repository: cline/cline#1
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 71024
---

Never perform blocking work — I/O, process waits, or network/IPC probes — while holding a lock that other threads need for non-blocking access. A thread blocked inside `write_all`, a D-Bus call, or `child.wait()` while holding a mutex stalls every other caller of that lock, including UI or IPC command threads. Offload blocking operations to a dedicated worker (e.g., a per-resource thread fed by an `mpsc` channel) so the lock only ever guards fast, in-memory state, and release locks before any call that can block or take unbounded time. When a blocking call is unavoidable on a thread others depend on (e.g., a GTK main-thread probe), run it on a separate thread and bound the wait with a timeout, deciding deterministically what "no answer in time" means.

When multiple locks protect related state, document and enforce a single acquisition order (e.g., "process before ws_endpoint, never the reverse") so no code path can deadlock by acquiring them in reverse order.

Guard against TOCTOU races: any check made before taking a lock (or before an async operation completes) must be re-verified immediately after acquiring the lock and immediately before the action it gates — e.g., recheck a shutdown flag under the lock before spawning, or re-validate a build/version epoch while holding the installation lock right before replacing a file. An unlocked check is only a hint; the authoritative decision must happen under the lock, right before the mutating action.

Finally, when concurrent replacement/cleanup of the same keyed resource (sessions, child processes) is possible — even only in theory — tag each instance with a generation or identity (pid, generation counter) and have cleanup code verify it still owns the current entry before removing or mutating it. This prevents a stale async callback from clobbering a newer resource that replaced it.

Example pattern from a terminal session manager:
```rust
// Don't hold the sessions lock across a blocking write.
// Instead, each session owns a writer thread fed by a channel:
struct TerminalSession {
    writer_tx: mpsc::Sender<Vec<u8>>, // enqueue only, never blocks the IPC thread
    generation: u64,
}

fn terminal_write(state: &Sessions, id: &str, data: Vec<u8>) -> Result<(), String> {
    let sessions = state.lock().unwrap();
    let session = sessions.get(id).ok_or("no such terminal")?;
    session.writer_tx.send(data).map_err(|_| "terminal closed".into())
    // lock is released immediately; the actual write happens on the writer thread
}

// Cleanup only removes the entry it created, even if another spawn replaced it:
fn on_reader_exit(sessions: &Sessions, id: &str, generation: u64) {
    let mut map = sessions.lock().unwrap();
    if map.get(id).is_some_and(|s| s.generation == generation) {
        map.remove(id);
    }
}
```