---
title: Fail loudly, resync state
description: Never let an operation silently succeed-in-appearance after a failure.
  Explicitly check the outcome of every async call or input validation, and on failure
  both surface a clear error and resync any dependent UI/application state — don't
  leave stale or inconsistent data behind.
repository: decolua/9router#probeA1
label: Error Handling
language: JavaScript
comments_count: 4
repository_stars: 31730
---

Never let an operation silently succeed-in-appearance after a failure. Explicitly check the outcome of every async call or input validation, and on failure both surface a clear error and resync any dependent UI/application state — don't leave stale or inconsistent data behind.

Concretely:
- Check `res.ok` / status codes before trusting a response body. If a fetch fails, report the error and rehydrate state from the source of truth instead of assuming the previous optimistic update is still valid.
  ```js
  const res = await fetch("/api/cli-tools/omp-settings", { method: "POST", body: ... });
  if (!res.ok) {
    setError("Failed to save models");
    await checkStatus(); // rehydrate instead of trusting local state
    return;
  }
  ```
- Avoid bare `catch { /* silent */ }` blocks that swallow errors. When a dependent fetch fails (e.g. "extras" only relevant when a feature is installed), clear/reset the related state on every failure path (not-installed, fetch error, outer fetch error), not just the happy path.
- Validate input shapes and status-code classifications strictly before branching logic acts on them. Ambiguous or malformed data (e.g. a string array misread as a byte array) should throw a clear, documented error rather than silently pass through and produce corrupted output.
- When the same validation/classification logic is used in multiple places (e.g. a "Test connection" probe and the actual request path), extract it into a single shared function so error classification can't drift between code paths.

Applying this consistently prevents silent data corruption, stale UI state, and divergence between validation and production code paths.