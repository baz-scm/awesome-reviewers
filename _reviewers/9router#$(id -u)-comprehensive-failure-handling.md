---
title: Comprehensive failure handling
description: Treat failure as a first-class path rather than an afterthought. When
  validating input, reject ambiguous or malformed shapes explicitly instead of letting
  them silently pass a loose check (e.g. an array of strings being coerced into a
  1-byte buffer that still satisfies a `length > 0` test) — if the shape is wrong,
  throw a clear error ("Invalid reference...
repository: decolua/9router#$(id -u)
label: Error Handling
language: JavaScript
comments_count: 4
repository_stars: 31730
---

Treat failure as a first-class path rather than an afterthought. When validating input, reject ambiguous or malformed shapes explicitly instead of letting them silently pass a loose check (e.g. an array of strings being coerced into a 1-byte buffer that still satisfies a `length > 0` test) — if the shape is wrong, throw a clear error ("Invalid reference image") instead of forwarding corrupted data downstream. When wiring error/fallback logic (interception, retries, finish-reason computation, etc.), make sure it runs on every code path that can produce the outcome you're guarding against, not just the most common one — e.g. a fallback that only lives in the non-streaming handler will silently miss the case where a provider is forced into streaming. Terminal/error states from upstream (failed, incomplete, timed out) must be detected explicitly and translated into a proper error response, with a sensible default error message when the upstream payload doesn't provide one, rather than falling through to success-path logic. Finally, always check the result of async operations (e.g. `res.ok` on a fetch) before updating local/persisted state; on failure, surface the error to the user and resynchronize state from the source of truth instead of assuming the call succeeded.

Example pattern to follow:
```js
const res = await fetch("/api/save", { method: "POST", body: JSON.stringify(payload) });
if (!res.ok) {
  const err = await res.json().catch(() => ({}));
  setError(err.message || "Save failed");
  await checkStatus(); // resync local state with the actual persisted state
  return;
}
```