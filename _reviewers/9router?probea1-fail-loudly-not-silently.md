---
title: Fail loudly, not silently
description: Code must never assume an operation succeeded or that input data is well-formed;
  it should explicitly validate and check status before proceeding, and surface/raise
  an error the moment an invariant is violated rather than letting bad data or a failed
  call silently flow through. This applies to both input validation (e.g. a loosely-typed
  branch that accepts...
repository: decolua/9router?probeA1
label: Error Handling
language: JavaScript
comments_count: 3
repository_stars: 31730
---

Code must never assume an operation succeeded or that input data is well-formed; it should explicitly validate and check status before proceeding, and surface/raise an error the moment an invariant is violated rather than letting bad data or a failed call silently flow through. This applies to both input validation (e.g. a loosely-typed branch that accepts a mixed string/byte array and converts it into a bogus 1-byte buffer instead of rejecting it) and async call results (e.g. ignoring `res.ok` on a fetch and assuming the POST succeeded). Concretely:

1. Validate the full shape/type of data before acting on it, and throw a clear, specific error for any unsupported or malformed input instead of letting it pass a loose check (e.g. `Uint8Array.from(["data:..."])` silently producing `[0]`). Add regression tests for the malformed-input case.
2. Always check the result/status of an async call or sub-operation before treating it as successful. On failure, surface the error to the user/caller and resync local/cached state from the source of truth (e.g. call `checkStatus()` again) rather than leaving stale optimistic state.
3. Keep failure domains isolated: a failure in one sub-check (e.g. `pip list` failing inside `getInstalledHeadroomExtras`) must not overwrite or corrupt an already-determined, unrelated success flag (e.g. `installed` from a separate binary probe). Merge partial results carefully so one failing subsystem can't flip unrelated state to a false failure.

Example:
```js
const res = await fetch("/api/cli-tools/omp-settings", { method: "POST", body: ... });
if (!res.ok) {
  const err = await res.json().catch(() => ({}));
  setMessage({ type: "error", text: err.message || "Failed to save models" });
  await checkStatus(); // rehydrate from server instead of trusting optimistic state
  return;
}
```