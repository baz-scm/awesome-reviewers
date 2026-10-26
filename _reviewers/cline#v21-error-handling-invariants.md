---
title: Error Handling Invariants
description: "Apply a single error-handling standard across the codebase:\n\n1) **Classify\
  \ errors precisely, don’t “make up” outcomes**\n   - Treat “missing/unresolvable”\
  \ as a specific class; everything else must surface (e.g., git show: only convert\
  \ “missing path/object/unknown revision” into “absent side”, but propagate buffer/IO/other\
  \ failures)."
repository: cline/cline#v21
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 70886
---

Apply a single error-handling standard across the codebase:

1) **Classify errors precisely, don’t “make up” outcomes**
   - Treat “missing/unresolvable” as a specific class; everything else must surface (e.g., git show: only convert “missing path/object/unknown revision” into “absent side”, but propagate buffer/IO/other failures).

2) **Preserve recovery invariants; never fall through after recovery decisions**
   - If an error-recovery path is meant to stop further work (e.g., don’t replace a live session if persistence/recovery did not fully succeed), ensure code returns/throws immediately—don’t rely on “rare null” behavior.
   - When you set transient state to enable recovery (e.g., staleness flags), clear it *before* the risky operation but **restore it if the risky operation throws**.

3) **Make async failures impossible to miss**
   - Never leave detached promises unhandled (especially inside “non-blocking” flows). Always `.catch(...)`, or keep the promise inside the existing try/catch.
   - When using `.then(attach, onError)`, also handle exceptions thrown *inside* attach/setup—otherwise they become unhandled rejections and can hang processes.
   - Ensure “kill/cleanup” paths never throw into the global unhandled-rejection channel; route failures through the same error reporting path used by normal failures.

4) **Retry semantics must be bounded and safe**
   - Don’t automatically treat timeouts as “retryable for whole-turn” without checking whether the provider may have processed the request.
   - Keep retry budgets/phase rules consistent with the underlying streaming/retry machinery; preserve existing diagnostics and limits.

Example pattern (route all async errors + preserve invariants):
```ts
async function safeOperation() {
  // invariant guard
  if (!readyForRetry) return; 

  transientFlag = false;
  try {
    await riskyRecovery();
  } catch (e) {
    transientFlag = true; // restore on failure
    throw e;
  }
}

// Detached async work: never leave unhandled rejections
void (async () => {
  try {
    await backgroundCommit();
  } catch (e) {
    logger.error('checkpoint commit failed', { e });
  }
})();

// Attach/setup: catch both rejection and thrown exception
loadSomething()
  .then((x) => {
    try { return attach(x); }
    catch (e) { throw e; }
  })
  .catch((e) => fail(e));
```

Adopting these rules prevents: misclassified failures masquerading as success, silent protection/recovery disablement, orphaned/duplicated runtime entities, hung processes from uncaught async errors, and incorrect retry behavior that can repeat side effects or distort attribution.