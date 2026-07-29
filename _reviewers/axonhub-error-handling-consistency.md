---
title: Error Handling Consistency
description: 'When handling failures, make error semantics explicit and consistent
  across the stack:


  - Define retryability precisely: only treat errors as retryable when you can guarantee
  it won’t duplicate already-delivered output (e.g., transport ended before a usable
  response). Add regression tests for each retry branch (positive + negative cases).'
repository: looplj/axonhub
label: Error Handling
language: Go
comments_count: 3
repository_stars: 4808
---

When handling failures, make error semantics explicit and consistent across the stack:

- Define retryability precisely: only treat errors as retryable when you can guarantee it won’t duplicate already-delivered output (e.g., transport ended before a usable response). Add regression tests for each retry branch (positive + negative cases).
- Avoid redundant status checks: if your HTTP client wrapper already converts non-2xx/3xx to errors, don’t re-check `StatusCode` in the caller; reserve parsing/"could not parse" errors for successful responses.
- Keep error construction consistent with local conventions: use the project’s existing error formatting/wrapping approach (e.g., `fmt.Errorf`) rather than introducing new error packages/types without an established convention.

Example pattern (retry classification):
```go
func isRetryableTransportError(err error) bool {
	if err == nil {
		return false
	}
	if errors.Is(err, io.EOF) || errors.Is(err, io.ErrUnexpectedEOF) {
		return true
	}
	var netErr net.Error
	return errors.As(err, &netErr) && (netErr.Timeout() || netErr.Temporary())
}
```
And ensure callers only retry when the failure occurs before output is committed, with tests covering `Timeout`, `Temporary`, and the “neither set” negative case.