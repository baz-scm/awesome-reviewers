---
title: Fail explicitly, never silently
description: 'Code must never let an error condition pass silently or leave the system
  in an inconsistent state. This applies to three common failure points: input validation,
  aggregating results from multiple sources, and handling async call outcomes.'
repository: decolua/9router#zz237855c
label: Error Handling
language: JavaScript
comments_count: 3
repository_stars: 31752
---

Code must never let an error condition pass silently or leave the system in an inconsistent state. This applies to three common failure points: input validation, aggregating results from multiple sources, and handling async call outcomes.

1. Validate inputs strictly before acting on them, and throw/return a clear error for any shape you don't explicitly support, instead of coercing it into something "valid-looking". For example, treating a string array as raw bytes produced `Uint8Array.from(["data:..."])`, a 1-byte buffer that passed a length check and silently sent a corrupted image to the provider instead of returning the expected 400.

2. When combining results from multiple independent probes/checks into one status object, don't let a failure in a secondary probe overwrite or mask an unrelated primary signal. If `pip list` fails while gathering extras, that should not flip an already-confirmed `installed: true` to `false`; keep each signal's provenance distinct and only merge in the parts that succeeded.

3. Always check the outcome of network/async calls (`res.ok`, status codes, resolved values) before updating local state or assuming success. On failure, surface the error to the user and resynchronize local state with the source of truth rather than leaving it stale or inconsistent:

```js
const res = await fetch("/api/cli-tools/omp-settings", { method: "POST", body: JSON.stringify({ models }) });
if (!res.ok) {
  const err = await res.json().catch(() => ({}));
  setMessage({ type: "error", text: err.message || "Failed to save models" });
  await checkStatus(); // rehydrate from server instead of trusting optimistic local state
  return;
}
```

Add regression tests for the failure paths (malformed input, partial probe failure, non-OK responses) to ensure errors are detected and handled rather than silently swallowed.