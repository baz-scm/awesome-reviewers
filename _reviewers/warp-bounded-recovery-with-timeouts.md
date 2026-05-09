---
title: Bounded Recovery With Timeouts
description: 'Implement failure handling so recovery is (1) bounded, (2) never hangs
  indefinitely, and (3) has explicit validation + deterministic fallback.


  Apply this when adding retries, polling for readiness, or supporting boundary-specific
  execution paths:'
repository: warpdotdev/warp
label: Error Handling
language: Markdown
comments_count: 3
repository_stars: 56893
---

Implement failure handling so recovery is (1) bounded, (2) never hangs indefinitely, and (3) has explicit validation + deterministic fallback.

Apply this when adding retries, polling for readiness, or supporting boundary-specific execution paths:

- Resource-bounded recovery: if you retry after a known quota/limit failure, ensure the retry does not keep consuming the same global budget. Make the retry’s accounting explicit (e.g., disable quota consumption for a bounded-scope retry or pass the correct remaining quota), and add a regression test for the triggering condition.
  ```rust
  // Pattern: on known limit failure, retry with bounded cost by adjusting quota.
  match err {
    ExceededMaxFileLimit => {
      // Retry only what’s needed at shallow depth; avoid consuming the global quota again.
      entry.build_tree(max_depth = 1, remaining_file_quota = None)?;
    }
    other => return Err(other.into()),
  }
  ```

- Timeout + actionable error: any polling loop / “wait until ready” / session-join wait must have a timeout and surface a clear error state when exceeded.
  ```rust
  let ready = tokio::time::timeout(Duration::from_secs(30), wait_for_ready()).await;
  match ready {
    Ok(Ok(())) => {}
    Ok(Err(e)) => return Err(e),
    Err(_) => return Err(anyhow::anyhow!("Timed out waiting for follow-up session readiness")),
  }
  ```

- Explicit validation and fallback: for boundary-specific spawning (WSL/MSYS2/remote/local) validate required arguments up front and ensure unsupported paths fail predictably (graceful unsupported-shell fallback) rather than relying on implied behavior.

- Test the failure mode: add regression tests that assert the system enters the correct recovered state (or correct failure state) under the exact triggering conditions (quota exceeded, hang/timeout scenario, unsupported-shell spawn path).