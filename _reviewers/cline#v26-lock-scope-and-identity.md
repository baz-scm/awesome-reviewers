---
title: Lock Scope And Identity
description: 'When concurrency involves long-running/blocking work and lifecycle replacement,
  follow four rules:


  1) **Do not hold shared locks across blocking IO/work**'
repository: cline/cline#v26
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 70893
---

When concurrency involves long-running/blocking work and lifecycle replacement, follow four rules:

1) **Do not hold shared locks across blocking IO/work**
- Keep the global lock scope small: lock → clone a handle/reference → release → then perform `write_all`, waits, network IO, etc.

2) **Offload blocking work to workers; use message passing for the boundary**
- If an IPC command (or UI/main-thread handler) would otherwise block, enqueue work to a per-session/per-resource worker thread via an `mpsc` channel. The command returns quickly; the worker owns the blocking write/read.

3) **Guard state mutations against out-of-order/lifecycle replacement**
- Late events (EOF, buffered “ready” lines, writer results) must not wipe or mutate the successor. Gate mutations on an identity/version you control (e.g., `child_pid`, per-session generation, or “still-current” check).

4) **Make lock order explicit and enforce it**
- If multiple locks exist, document a strict lock acquisition order (and ensure every code path respects it), especially around retries, shutdown, and replacement flows.

Example pattern (writer offload + generation gating):

```rust
// Shared map: id -> (generation, tx)
type Sessions = Arc<Mutex<HashMap<String, (u64, std::sync::mpsc::UnboundedSender<Vec<u8>>)>> >;

fn terminal_write(sessions: &Sessions, id: &str, gen: u64, data: Vec<u8>) -> Result<(), String> {
    // 1) lock briefly: clone tx; release before send/write
    let tx = {
        let map = sessions.lock().map_err(|e| e.to_string())?;
        let (stored_gen, tx) = map.get(id).ok_or("missing session")?;
        if *stored_gen != gen { return Err("stale session".into()); }
        tx.clone()
    };
    // 2) enqueue; worker thread does blocking IO
    tx.send(data).map_err(|e| e.to_string())
}

fn session_worker(rx: impl Iterator<Item = Vec<u8>>, mut pty_writer: impl std::io::Write) {
    for chunk in rx {
        // blocking write happens here, not under the shared map lock
        let _ = pty_writer.write_all(&chunk);
    }
}
```

Adopting this standard prevents: IPC/UI stalls from blocked IO, deadlocks from unclear lock ordering, and correctness bugs where late events from an old child/session clobber the state of a new one.