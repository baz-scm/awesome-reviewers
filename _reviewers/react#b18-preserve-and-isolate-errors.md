---
title: Preserve and isolate errors
description: 'When catching exceptions, be deliberate about what is caught and never
  discard useful error information:


  1. **Never swallow the original error silently.** If you log or rethrow a new error
  after a catch, attach the original as context so the real failure is still visible:'
repository: facebook/react#b18
label: Error Handling
language: JavaScript
comments_count: 8
repository_stars: 251889
---

When catching exceptions, be deliberate about what is caught and never discard useful error information:

1. **Never swallow the original error silently.** If you log or rethrow a new error after a catch, attach the original as context so the real failure is still visible:
```js
try {
  inspect();
} catch (error) {
  return {error: new Error('Failed to inspect hooks.', {cause: error})};
}
```
A bare `catch {}` or a message that doesn't include the caught error (e.g. "eval() is not supported...") hides the real cause and makes debugging much harder.

2. **Only catch the specific condition you expect, and rethrow everything else.** Don't use a catch block to blanket-suppress all failures when only one failure mode is recoverable:
```js
try {
  unlinkSync(path);
} catch (err) {
  // Only an expected, recoverable condition should be swallowed.
  if (err.code !== 'ENOENT') {
    throw err;
  }
}
```
Similarly, prefer surfacing unexpected failures (warn or fail the build/process) rather than silently falling back and producing a different, unexplained result.

3. **Never make error handling conditional on `__DEV__`.** Throwing only in development is inconsistent and surprising; use `console.error` for dev-only diagnostics instead of `throw`.

4. **Isolate failures so one error doesn't take down unrelated work**, and use `try/finally` to guarantee cleanup (e.g. releasing a pending callback/map entry) even when the operation throws:
```js
try {
  callback(response);
} finally {
  evalRequestCallbacks.delete(requestId);
}
```
When invoking multiple independent callbacks or instruction handlers, wrap each individually in its own try/catch so a failure in one does not prevent the others from running.

Applying these rules consistently keeps error messages actionable, prevents accidental masking of real bugs, and avoids resource leaks or cascading failures caused by overly broad or careless error handling.