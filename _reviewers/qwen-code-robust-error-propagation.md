---
title: Robust error propagation
description: When handling failures, ensure you (a) don’t lose the real root cause,
  (b) never introduce new exceptions while trying to report one, and (c) keep graceful
  degradation both implemented and tested.
repository: QwenLM/qwen-code
label: Error Handling
language: JavaScript
comments_count: 7
repository_stars: 26407
---

When handling failures, ensure you (a) don’t lose the real root cause, (b) never introduce new exceptions while trying to report one, and (c) keep graceful degradation both implemented and tested.

Apply these rules:
- Check all failure channels from process execution (e.g., `spawnSync`/`execSync`): if `result.error` exists, log it and return/exit predictably; don’t infer a transport failure from empty stdout.
- Keep error variables in correct scope: if a later block needs the last failure, store it outside the `catch` (e.g., `let lastError; ... catch (e) { lastError = e; }`).
- Preserve original context when rethrowing/wrapping: use `new Error(message, { cause: lastError })` so stacks/types aren’t discarded.
- Avoid fragile string coupling for control flow (retryability, classification): define a shared constant for message identifiers rather than comparing against raw throw-text.
- Deduplicate repeated error-message construction (e.g., a `deadlineError()` helper) to keep error formatting consistent.
- For “best-effort” steps that must not fail the whole workflow (especially under `always()`), include fallback guards (e.g., `|| echo "...continuing."`) and assert them in tests.

Example pattern (scope-safe + preserve cause):
```js
function deadlineError(lastError) {
  return new Error(
    `Model generation time budget exhausted: ${lastError?.message ?? 'unknown error'}`,
    { cause: lastError },
  );
}

let lastError;
for (;;) {
  if (Date.now() >= deadline) throw deadlineError(lastError);
  try {
    // ...
  } catch (e) {
    lastError = e;
    // retry / backoff
  }
}
```

Checklist for review:
1) Are all error sources checked (not just stdout/text)?
2) Can any error-reporting path throw a new exception (scope/ReferenceError)?
3) Do wrapped errors include `{ cause }`?
4) Are control-flow decisions based on stable identifiers (constants), not rewordable strings?
5) Are fallback/best-effort behaviors covered by assertions in tests?
6) Is error-message construction centralized to avoid drift?