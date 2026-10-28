---
title: Safe stale-lock recovery
description: When using directory- or file-based locks for cross-process mutual exclusion
  (e.g., atomic `mkdir` as a lock), never rely on simple existence or mtime alone
  to decide a lock is "stale." Record the owner's identity (PID plus process start
  time, since PIDs can be reused) when the lock is acquired, and use that to determine
  liveness.
repository: cline/cline#&&sleep 4
label: Concurrency
language: Shell
comments_count: 3
repository_stars: 70980
---

When using directory- or file-based locks for cross-process mutual exclusion (e.g., atomic `mkdir` as a lock), never rely on simple existence or mtime alone to decide a lock is "stale." Record the owner's identity (PID plus process start time, since PIDs can be reused) when the lock is acquired, and use that to determine liveness.

Reclaiming an abandoned lock is inherently racy: a contender may observe a stale lock, but by the time it acts, another process may have already claimed it. To avoid double-reclaim or corrupting a live lock:
1. Claim the *right* to reclaim atomically (e.g., `mkdir` a `reclaim` marker inside the specific lock directory, not a generically-named one).
2. Re-read the owner info from that exact lock path and re-verify it is still the same stale owner before moving/removing it.
3. Only proceed if the lock you are about to destroy is still identically the one you inspected (e.g., via inode/`-ef` checks), never a cached reference that could now point to a different, live lock.

Always operate on absolute, canonicalized paths for lock files/directories. Relative paths combined with subshell `cd` or working-directory changes can cause identity checks (e.g., `-ef` comparisons) to silently fail, breaking the recovery logic. Normalize user-supplied paths (such as `--install-dir`) to absolute paths before constructing any lock path.

Ensure cleanup handlers (`trap ... EXIT INT TERM`) remove only locks owned by the current process, and clean up temporary artifacts (e.g., partial downloads) on exit. Add regression tests that simulate concurrent lock contention and abandoned-lock recovery, including cases with relative paths and successor processes replacing an observed stale lock, to confirm recovery never clobbers a live owner.