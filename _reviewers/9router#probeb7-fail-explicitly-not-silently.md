---
title: Fail explicitly, not silently
description: When an operation can fail or receive malformed input, never let it silently
  degrade into an incorrect-but-successful-looking result. Validate input shapes strictly
  before processing (don't assume an array of strings is an array of bytes), check
  return/response status on every network or async call (`res.ok`, error codes), and
  keep unrelated state isolated...
repository: decolua/9router#probeB7
label: Error Handling
language: JavaScript
comments_count: 3
repository_stars: 31737
---

When an operation can fail or receive malformed input, never let it silently degrade into an incorrect-but-successful-looking result. Validate input shapes strictly before processing (don't assume an array of strings is an array of bytes), check return/response status on every network or async call (`res.ok`, error codes), and keep unrelated state isolated so a failure in one sub-check can't corrupt an already-known-good value elsewhere.

Concretely:
- Validate the exact shape/type of inputs before acting on them, and throw/return a clear error for anything that doesn't match, rather than coercing bad data into a "valid-looking" result (e.g. don't let `Uint8Array.from(["data:..."])` quietly produce a 1-byte buffer that passes a length check).
- When combining results from multiple independent probes/checks, don't let a failure in one (e.g. `pip list` failing) overwrite or flip the status of another that was already verified successfully. Merge only the fields each check is responsible for.
- Always check the success/failure of async calls before updating local/UI state. On failure, surface the error to the user and reconcile state with the source of truth instead of assuming the optimistic update succeeded.

Example:
```js
async function saveModels(models) {
  const res = await fetch("/api/cli-tools/omp-settings", { method: "POST", body: JSON.stringify({ models }) });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    setMessage({ type: "error", text: err.message || "Failed to save models" });
    await checkStatus(); // rehydrate from server instead of trusting optimistic state
    return;
  }
  setSelectedModels(models);
}
```
Applying this consistently prevents confusing downstream failures (bad data reaching external APIs, incorrect dashboard status, UI state drifting from persisted state) and makes failure modes visible and debuggable.