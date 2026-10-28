---
title: Lock discipline and blocking ops
description: 'Shared mutable state must be protected with clear, documented rules
  so locks never become a source of deadlocks or stalls:


  1. Never hold a lock across a blocking call. If a write/read/spawn can block indefinitely
  (a PTY write to a stalled shell, a child process spawn), release the lock before
  the blocking call, or move the blocking work onto its own...'
repository: cline/cline#`sleep 4`
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 70979
---

Shared mutable state must be protected with clear, documented rules so locks never become a source of deadlocks or stalls:

1. Never hold a lock across a blocking call. If a write/read/spawn can block indefinitely (a PTY write to a stalled shell, a child process spawn), release the lock before the blocking call, or move the blocking work onto its own dedicated thread fed by a channel so the lock-holding command thread only enqueues work and returns immediately.
   ```rust
   // Bad: write_all can block while holding the sessions lock
   let mut sessions = state.sessions.lock().unwrap();
   sessions.get_mut(&id).unwrap().writer.write_all(data.as_bytes())?;

   // Good: a dedicated writer thread owns the blocking call; the command
   // only enqueues and returns immediately.
   session.writer_tx.send(data)?; // writer thread does write_all
   ```

2. When more than one lock can be involved in an operation, document and enforce a single, consistent acquisition order (e.g. "`process` may be held while acquiring `ws_endpoint`, never the reverse") so every call site that touches both locks follows it. Prefer taking locks strictly sequentially over nesting when possible.

3. Treat "check, then act" as unsafe unless the check is re-validated under the same lock used for the act. A flag or condition observed outside a lock can change before the lock is acquired (e.g. a shutdown flag set between an unlocked check and a locked spawn); re-check it immediately after acquiring the lock that guards the mutation.

4. When identifiers or resources can be concurrently replaced (e.g. a session id reused, a child process respawned), tag each instance with a generation/version and have background threads only act on, or remove, the version they were started with — never unconditionally overwrite or delete by key alone, since a stale thread could clobber a newer instance.

5. When a background thread races against a timeout (e.g. probing a D-Bus service from a UI thread), run the blocking work off-thread and bound the wait with `recv_timeout` or an equivalent, and explicitly document which outcome the ambiguous timeout case should resolve to and why, so the tradeoff is intentional rather than accidental.

Applying these rules prevents stalled UI/IPC threads, deadlocks from inconsistent lock ordering, and subtle races where stale background work corrupts newer state.</description>
