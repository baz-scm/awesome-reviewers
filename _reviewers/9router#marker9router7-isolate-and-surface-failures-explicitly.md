---
title: Isolate and surface failures explicitly
description: When combining results from multiple sub-operations (probes, API calls,
  streaming events), never let a failure in one operation silently corrupt or overwrite
  state produced by another successful operation. Each operation's success/failure
  must be checked and handled independently, with explicit fallback behavior for the
  failure case rather than assuming...
repository: decolua/9router#MARKER9ROUTER7
label: Error Handling
language: JavaScript
comments_count: 3
repository_stars: 31425
---

When combining results from multiple sub-operations (probes, API calls, streaming events), never let a failure in one operation silently corrupt or overwrite state produced by another successful operation. Each operation's success/failure must be checked and handled independently, with explicit fallback behavior for the failure case rather than assuming success.

Concretely:
- When merging data from several sources into one result object, keep each source's own success/failure status intact. For example, if a CLI probe says a tool is `installed`, a secondary lookup (e.g. `pip list`) failing should not flip `installed` back to `false`; only merge the fields that the secondary call is actually responsible for.
- When an async operation (fetch, upstream stream event) can fail, always check the response/status (`res.ok`, `response.status === "incomplete"`, etc.) before treating it as success. On failure, emit a clear error (with a sensible fallback message if the upstream doesn't provide one) and resynchronize local/UI state with the source of truth instead of leaving it in an inconsistent, optimistic state.
- Add regression tests covering the failure/error paths (not just the happy path) to prevent regressions.

Example:
```js
const res = await fetch("/api/cli-tools/omp-settings", { method: "POST", body });
if (!res.ok) {
  const err = await res.json().catch(() => ({}));
  setMessage({ type: "error", text: err.message || "Failed to save models" });
  await checkStatus(); // resync UI with actual persisted state
  return;
}
```