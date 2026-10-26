---
title: Error Handling Contracts
description: Adopt error-handling contracts that prevent *silently wrong outcomes*
  (fake successes, misleading UI), *uncaught async failures* (unhandled rejections/EPIPE),
  and *incorrect recovery* (retries that duplicate side effects or lose already-executed
  results).
repository: cline/cline#v6
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 70864
---

Adopt error-handling contracts that prevent *silently wrong outcomes* (fake successes, misleading UI), *uncaught async failures* (unhandled rejections/EPIPE), and *incorrect recovery* (retries that duplicate side effects or lose already-executed results).

**Standard rules**
1. **No fallthrough after invariant checks**: if an invariant is “should never be missing,” throw (or return) instead of continuing into a path that can mutate state.
2. **Classify errors before synthesizing UI/state**:
   - Only treat truly-missing resources as “missing” (e.g., path/object not found).
   - Any other failure (timeouts, size caps, transport limits) must propagate as an actual error; do not render it as a deletion/truncation unless explicitly marked.
3. **Recovery/retry must be boundary-aware**:
   - Distinguish *pre-dispatch* vs *post-dispatch confirmed* actions so the UI doesn’t offer “resend” that duplicates an already-sent request.
   - Preserve already-executed tool activity/results across retries; never replay local side effects from an unfinished transient response.
4. **Contain async failures**:
   - No unhandled promise rejections: any detached async work must attach error handling and must not leave the UI in a “success” state without required data.
   - Handle stream/pipe errors (stdin/stdout) with listeners so EPIPE/write failures don’t crash the host.
   - Telemetry/instrumentation must be non-blocking: if it fails or throws, inference and core operations must continue.
5. **Security-affecting settings must not fail silently**:
   - If config is unreadable/corrupt, don’t automatically disable protection without logging or surfacing a warning; distinguish “absent” vs “unreadable.”

**Reusable patterns**
- **Cover exceptions thrown inside success callbacks**
```ts
void loadMxc()
  .then((mxc) => mxc.spawn(/*...*/))
  .then((sandboxed) => handle.attach(sandboxed)) // attach can throw
  .catch((err) => {
    handle.fail(new Error(`Sandboxing failed: ${String(err)}`));
  });
```
- **Handle detached promises (no unhandled rejections)**
```ts
this.say('checkpoint_created');
void this.checkpointTracker.commit()
  .then((hash) => {
    if (!hash) return;
    return this.messageStateHandler.updateClineMessage(/*...*/);
  })
  .catch((err) => {
    console.error('checkpoint commit failed', err);
  });
```
- **Differentiate “not found” vs “other failure” before rendering**
```ts
const text = await gitShow().catch((e) => {
  if (isMissingPathOrObject(e)) return undefined;
  throw e; // real error
});
```

**Outcome**
These rules make error paths deterministic: failures don’t masquerade as success, retries don’t duplicate side effects, and auxiliary failures (streams/telemetry) can’t bring down the host or abort the core workflow.