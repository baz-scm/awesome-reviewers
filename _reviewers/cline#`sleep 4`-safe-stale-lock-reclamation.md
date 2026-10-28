---
title: Safe stale-lock reclamation
description: 'When implementing cross-process locks (e.g., directory-based mutexes
  in shell scripts), guard against races during both acquisition and stale-lock recovery:'
repository: cline/cline#`sleep 4`
label: Concurrency
language: Shell
comments_count: 3
repository_stars: 70979
---

When implementing cross-process locks (e.g., directory-based mutexes in shell scripts), guard against races during both acquisition and stale-lock recovery:

1. Encode true ownership in the lock, not just its existence. Store the owner's PID plus process start time (not just mtime), since PIDs can be reused and timestamps alone are unreliable: `owner="$$ $(TZ=UTC ps -p $$ -o lstart=)"`.

2. Before reclaiming a lock that appears abandoned, perform a double-checked claim: atomically mark that you are attempting recovery (e.g., `mkdir "$lock/reclaim"`), then re-read and re-verify the owner/identity *after* that claim succeeds. Only proceed if the lock still matches what you originally observed as stale — otherwise a legitimate new owner may have taken it in the meantime, and reclaiming would corrupt its state.

3. Always resolve any user-supplied or relative paths to absolute paths *before* constructing lock paths or entering subshells that rely on identity checks (e.g., `-ef` comparisons, `cd` + relative lookups). Relative paths silently break identity verification when the working directory changes between checks.

4. Ensure cleanup is deterministic and guaranteed: register an `EXIT`/`INT`/`TERM` trap that removes only locks/temp files owned by the current process, never a lock that may now belong to another contender.

5. Add regression tests that simulate real races: a stale lock replaced by a live successor during recovery, and recovery operating on relative vs. absolute paths — verify the original/live owner is never disturbed and no duplicate work (e.g., duplicate installs) occurs.

Example pattern for safe reclamation:
```bash
if [[ "$stale" == true ]]; then
    (
        cd "$lock" 2>/dev/null || exit 0
        mkdir reclaim 2>/dev/null || exit 0   # only one contender wins this claim
        current=$(cat owner 2>/dev/null || true)
        # re-verify identity/staleness AFTER claiming recovery, not before
        [[ "$current" == "$previous" && "$lock" -ef . ]] || exit 0
        # safe to reclaim now
    )
fi
```
This pattern generalizes beyond shell: any lock-recovery logic must re-validate state after claiming the right to act, not rely on a single stale read.</description>
</invoke>
