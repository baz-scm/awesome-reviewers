---
title: Propagate and Test Errors
description: 'Handle errors at the right boundary, keep failure state consistent,
  and ensure tests validate the real semantics.


  Apply these rules:

  1) Don’t swallow errors inside reusable helpers.'
repository: tanstack/query
label: Error Handling
language: JavaScript
comments_count: 3
repository_stars: 49380
---

Handle errors at the right boundary, keep failure state consistent, and ensure tests validate the real semantics.

Apply these rules:
1) Don’t swallow errors inside reusable helpers.
- If a helper is part of your public API (e.g., a function consumers can intentionally call), catching and only logging can hide failures from the caller.
- Prefer catching at the specific fetch boundary you’re trying to protect (e.g., automatic/refetch flows), and either rethrow or return a rejected promise so callers can detect failures.

Example (pattern):
```js
export async function refetchAllQueries({ queryCache }) {
  return Promise.all(
    queryCache.getAll().map(query =>
      query.fetch({ force: true })
    )
  );
}

// In the caller/boundary where automatic fetching should not crash:
refetchAllQueries({ queryCache }).catch(err => {
  console.error(err?.message ?? err);
  // keep error observable to the boundary’s own logic
});
```

2) Make failure metrics deterministic.
- If you track `failureCount`, reset it in the same place you mark a request as successful (e.g., in `actionSuccess`), rather than relying on an extra action that may not be wired through correctly.

3) Ensure tests genuinely exercise error-handling behavior.
- For retry logic, don’t write assertions that would pass accidentally due to incorrect assumptions (e.g., treating `retry` as a boolean when it can be a function).
- Structure tests so they would fail if retry semantics (like `retry: (failureCount, error) => ...`) aren’t implemented.

Result: callers can detect failures, internal failure state doesn’t drift, and tests accurately guard the intended error-handling semantics.