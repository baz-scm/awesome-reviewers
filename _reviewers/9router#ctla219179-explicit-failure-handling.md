---
title: Explicit failure handling
description: 'Never let a failed operation pass as success or leave the system in
  a silently inconsistent state. This applies both to network/response handling and
  to input validation:'
repository: decolua/9router#ctlA219179
label: Error Handling
language: JavaScript
comments_count: 5
repository_stars: 31730
---

Never let a failed operation pass as success or leave the system in a silently inconsistent state. This applies both to network/response handling and to input validation:

1. **Check results, don't assume success.** After any fetch/POST, inspect the response status (`res.ok`) before updating state. On failure (or in `catch` blocks), surface the error and resync local/UI state to match the server (e.g., re-run a status check) instead of leaving stale data displayed. For example, if `saveModels` POSTs and gets a 400 because the model list is empty, don't leave the UI showing "no models" while the backend still has the old `models.yml` — either reject the empty-save client-side or rehydrate from `checkStatus()` on failure.

2. **Validate inputs rigorously before trusting them.** Don't let loosely-typed or ambiguous data silently coerce into a "valid-looking" value that bypasses the intended error path. For example, `Uint8Array.from(["data:image/png;base64,..."])` produces a 1-byte array that passes a `.length` check but is garbage — only take the "raw bytes" branch when every element is actually an integer 0-255, otherwise throw/return the proper error (e.g., HTTP 400) before doing any further work (like a network fetch).

3. **Guard against ambiguous/overlapping identifiers before acting.** When injecting or substituting behavior (e.g., a fallback tool name), check for collisions with existing names first and skip the substitution entirely if there's a conflict, rather than risk executing the wrong logic under a shared identifier.

4. **Classify error codes deliberately, not generically.** When interpreting upstream status codes for health/validation probes, explicitly enumerate which codes represent real failures vs. transient/expected conditions (e.g., 429/500/502/503/504 should count as "valid" transient issues, not failures) rather than relying on broad includes/excludes that misclassify edge cases. Keep this logic centralized so different call sites (e.g., a "Test connection" button and the actual request path) can't drift apart on what counts as success vs. failure.

In short: treat every error branch as a first-class path — check it, classify it correctly, and restore/report consistent state rather than letting bad data or failed calls silently propagate as if they succeeded.</description>
</invoke>
