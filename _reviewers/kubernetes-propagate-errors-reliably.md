---
title: Propagate Errors Reliably
description: 'When implementing error-prone control flow (cleanup helpers, retries/polls,
  orchestration, allocation paths), do not hide failures.


  **Coding standard**'
repository: kUbernetes/kUbernetes
label: Error Handling
language: Go
comments_count: 6
repository_stars: 128688
---

When implementing error-prone control flow (cleanup helpers, retries/polls, orchestration, allocation paths), do not hide failures.

**Coding standard**
1. **Return errors from helpers used by orchestration/teardown**
   - Especially for test cleanup hooks (or any “finally/cleanup” style callback), return non-idempotent errors so the caller can fail the operation.
   - Only ignore errors you’ve explicitly deemed idempotent (commonly `NotFound`), and document that choice.

2. **Never discard failing errors from inner calls**
   - Avoid patterns like `x, _ := mayFail()` unless you *prove* it cannot fail in this context.
   - If ignoring is intentional, add a comment stating the invariant.

3. **Retries/polls must preserve meaningful failure information**
   - When returning from a function that retries until a deadline, return the last meaningful error or the timeout error—don’t replace it with `nil`.

4. **Make errors actionable**
   - Include the key quantities that explain the failure (e.g., requested vs retained/available) instead of generic messages.

**Example: cleanup helper (return errors, ignore only NotFound)**
```go
func deletePodImmediately(ctx context.Context, podClient *e2epod.PodClient, podName string) error {
	// Force-delete so namespace teardown doesn't block on intentional container outlives SIGTERM.
	err := podClient.Delete(ctx, podName, *metav1.NewDeleteOptions(0))
	if apierrors.IsNotFound(err) {
		return nil // idempotent: pod already gone
	}
	return err // non-NotFound failures must fail the spec/caller
}
```

**Example: preserving poll errors (don’t return nil)**
```go
for {
	ok, err := pollOnce()
	if ok {
		return true, nil
	}
	if err != nil {
		lastErr = err
		// keep retrying until deadline; do not erase lastErr
	}
	if time.Now().After(deadline) {
		return false, lastErr // or deadline error
	}
}
```

Adopting this consistently prevents “silent failure” classes: hidden cleanup regressions, misleading retry outcomes, and far-away error surfacing that makes production incidents much harder to debug.