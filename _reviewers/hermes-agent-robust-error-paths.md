---
title: Robust error paths
description: When handling errors, ensure you don’t (1) mask the original failure,
  (2) violate the intended timeout/retry/cleanup boundaries, or (3) make recovery
  decisions without explicit evidence.
repository: nousresearch/hermes-agent
label: Error Handling
language: Python
comments_count: 7
repository_stars: 221948
---

When handling errors, ensure you don’t (1) mask the original failure, (2) violate the intended timeout/retry/cleanup boundaries, or (3) make recovery decisions without explicit evidence.

**Standards**
1) **Cleanup must never throw / must not mask the real exception**
   - Initialize fields used in `finally` (e.g., worker/thread handles) or guard with `getattr`.
   - Never let error-handling or teardown code raise unless you are explicitly replacing the original error.

   ```python
   class Runner:
       def __init__(self):
           self._tts_playback_thread = None  # initialize for finally safety

       def run(self):
           try:
               ...
           finally:
               t = getattr(self, "_tts_playback_thread", None)
               if t and t.is_alive():
                   t.join(timeout=5)
   ```

2) **Honor deadlines everywhere (especially after streaming/pipes hit EOF)**
   - Don’t “fall through” into unbounded waits after partial progress.
   - Keep a single deadline source of truth and ensure the termination path is always reachable.

3) **Cleanup must cover the full resource scope**
   - If you spawn detached/different process trees, terminate the **process group** (or equivalent scope), not only the parent PID.
   - For multi-step operations, ensure the rollback/cleanup is consistent with the failure point.

4) **Recovery decisions must be evidence-gated**
   - Separate “definitive miss” from “inconclusive probe.” Only trigger fallback when probes are inconclusive (or when the code explicitly models the condition).
   - Avoid broad `except Exception` that collapses unrelated failures into the same recovery.

5) **Error ordering: validate ‘not found’ before operations that can raise 400/validation/unknown-task errors**
   - Ensure the API returns the intended status (e.g., 404 for missing task) by checking existence before calling functions that validate inputs and may raise.

6) **Preserve best-effort behavior where it was intentional**
   - If a route/feature previously returned a partial result on transient DB/tool errors, keep that contract; don’t replace best-effort with hard failure unless the user-visible contract changes.

Applying this standard will prevent masked exceptions, unblock deterministic cleanup/timeout behavior, and keep recovery logic correct and testable.