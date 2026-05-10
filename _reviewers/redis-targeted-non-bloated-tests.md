---
title: Targeted, Non-Bloated Tests
description: When adding/modifying tests, ensure they are (a) semantically aligned
  to the behavior under test, (b) precise enough to prove the intended code path was
  executed, and (c) not bloated or duplicated.
repository: redis/redis
label: Testing
language: Other
comments_count: 6
repository_stars: 74261
---

When adding/modifying tests, ensure they are (a) semantically aligned to the behavior under test, (b) precise enough to prove the intended code path was executed, and (c) not bloated or duplicated.

Apply this checklist:
1) **One behavior per test/subcase**: the scenario should directly relate to the option/feature being tested (avoid mixing unrelated parameters).
2) **Assert what proves the branch**: verify specific, narrow indicators (exact error substrings, distinctive log messages, or exact state transitions). Don’t rely only on “command succeeded.”
3) **Avoid coverage-masking fallbacks**: don’t use broad `catch`/fallback logic that allows the test to pass when the targeted flow didn’t occur.
4) **Consolidate instead of multiplying**: prefer reusing setup helpers and merging similar checks; remove duplicates and don’t add “for every command” coverage when broader tooling already exists.
5) **Keep expectations robust**: if output may differ slightly, match stable substrings rather than brittle full-text matches.

Example pattern (branch proof, not permissive fallback):
```tcl
# Good: only accept success if the targeted log line is present.
wait_for_log_messages -2 "*Disconnecting timedout replica (full sync)*" $loglines 100 100
# Later for the specific subcase:
wait_for_log_messages -2 "*Diskless rdb transfer, last replica dropped, killing fork child*" $loglines 1 1
```

If you need to reduce flakiness, do it by making the test deterministic (timing/config/input shaping), not by weakening the assertions that demonstrate the intended behavior was reached.