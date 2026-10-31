---
title: Explicit failure detection and recovery
description: Never let an async operation's success be assumed; always check the actual
  result (`res.ok`, exit status, response fields) before trusting its data, and apply
  that check consistently on every code path that can produce the failure — not just
  the first one you tested. When a secondary/less-critical check fails (e.g. `pip
  list` probing extras), don't let it...
repository: 'decolua/9router#

  exit 1'
label: Error Handling
language: JavaScript
comments_count: 5
repository_stars: 31737
---

Never let an async operation's success be assumed; always check the actual result (`res.ok`, exit status, response fields) before trusting its data, and apply that check consistently on every code path that can produce the failure — not just the first one you tested. When a secondary/less-critical check fails (e.g. `pip list` probing extras), don't let it override or corrupt state already established by a primary successful check; merge results carefully so one failing sub-check degrades only its own piece of state. On any failure branch, reconcile application/UI state to match reality — clear stale data, show an explicit error, and/or re-fetch the source of truth — instead of leaving previously-cached values that no longer reflect the backend. For terminal/error events (e.g. a failed streaming response), route them explicitly into an error path with a guaranteed fallback message when the upstream source omits one, rather than falling through to a generic "success" code path.

Example:
```js
async function saveModels(models) {
  const res = await fetch("/api/cli-tools/omp-settings", { method: "POST", body: JSON.stringify({ models }) });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    setMessage({ type: "error", text: err.message || "Failed to save models" });
    await checkStatus(); // rehydrate from server truth instead of trusting local state
    return;
  }
  setSelectedModels(models);
}
```
Apply this pattern to every fetch/subprocess/stream call: check the result, propagate/log the error, and resync state — on all return sites, not just the happy path.