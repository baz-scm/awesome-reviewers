---
title: Resync state on failure
description: 'When an async operation (API fetch, upstream event, or mutation) can
  fail or return a non-success status, don''t let the UI or downstream state silently
  drift from the true source of truth. Always check the result explicitly (e.g. `res.ok`,
  an upstream error/incomplete status) before trusting it, and on failure:'
repository: decolua/9router?x
label: Error Handling
language: JavaScript
comments_count: 3
repository_stars: 31748
---

When an async operation (API fetch, upstream event, or mutation) can fail or return a non-success status, don't let the UI or downstream state silently drift from the true source of truth. Always check the result explicitly (e.g. `res.ok`, an upstream error/incomplete status) before trusting it, and on failure:
1. Surface the error (emit an explicit error chunk/message, and provide a sane fallback message if the upstream/caller omitted one).
2. Reset or rehydrate any local/cached state so it reflects reality rather than stale or partial data — don't leave previous values (version info, extras, saved config) displayed as if they are still valid when the underlying call failed, was skipped, or the precondition (e.g. "feature not installed") no longer holds.

For example, when persisting settings:
```js
const res = await fetch("/api/cli-tools/omp-settings", { method: "POST", body: JSON.stringify({ models }) });
if (!res.ok) {
  const err = await res.json().catch(() => ({}));
  setMessage({ type: "error", text: err.message || "Failed to save settings." });
  await checkStatus(); // rehydrate from server instead of trusting optimistic local state
  return;
}
```
Similarly, when a dependent fetch fails or a feature is not installed, clear any related cached state (`setExtras(null)`, `setPendingExtras([])`) instead of leaving old values in place. This prevents inconsistent UI, stale cached data, and swallowed errors that mask real failures from users and future debugging.</description>
</invoke>
