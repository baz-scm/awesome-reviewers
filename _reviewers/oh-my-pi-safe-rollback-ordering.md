---
title: Safe rollback ordering
description: When a function performs a multi-step mutation of shared, possibly concurrently-accessed
  state (e.g., registering or rolling back a worktree on disk), handle failures so
  the system is never left in an ambiguous or unsafe state, and never mistake "error"
  for "expected absence."
repository: can1357/oh-my-pi
label: Error Handling
language: Rust
comments_count: 4
repository_stars: 37317
---

When a function performs a multi-step mutation of shared, possibly concurrently-accessed state (e.g., registering or rolling back a worktree on disk), handle failures so the system is never left in an ambiguous or unsafe state, and never mistake "error" for "expected absence."

1. Classify errors precisely before acting on them. Don't swallow every failure into the same "not present" case just because a missing file is one legitimate cause. For example, reading an optional setup-marker file should treat "file not found" as "no mark," but any other I/O error (e.g., the marker is unreadable or is actually a directory) must propagate as a real failure instead of being silently treated as "setup finished," which could let another process unsafely reuse the resource.

2. When rolling back a partially-completed operation, order the cleanup steps so that at every intermediate point other processes see either a fully valid state or an unambiguously invalid/locked one — never something that looks available or complete. For instance, when undoing a worktree registration, remove the back-reference (`gitdir`) before anything else so no process can list or take over the entry; only remove the checkout/registration once you're sure nothing else can race with it.

3. If a rollback step itself fails, stop there and leave the resource in its last known-safe state (e.g., still locked and marked with its live owner) rather than continuing and producing a half-cleaned, ambiguous result. Surface the original error so the caller/operator can recover (e.g., via manual `git worktree remove`), instead of silently discarding it.

4. Validate preconditions robustly against the actual resolved state, not just the literal input — e.g., canonicalize paths (including symlinked ancestors) before comparing a destination against a source, so error conditions like "destination is inside source" are reliably detected rather than missed due to superficial path differences.

Example pattern for staged writes with rollback:
```rust
let written: Result<()> = (|| {
    fs::write(admin.join("locked"), "initializing\n")?;
    if let Some(owner) = setup_owner {
        fs::write(admin.join(SETUP_MARK), format!("{owner}\n"))?;
    }
    fs::write(path.join(".git"), gitdir_line)?;
    fs::write(admin.join("gitdir"), back_reference)?;
    Ok(())
})();
if let Err(err) = written {
    // Remove the back-reference first so nothing else can see/take over
    // a half-written, locked entry; only then clean up the rest.
    let _ = fs::remove_dir_all(&admin);
    return Err(err);
}
```
Applying this discipline prevents silent data corruption, race conditions between concurrent processes, and unrecoverable partial states after a failure.</description>
