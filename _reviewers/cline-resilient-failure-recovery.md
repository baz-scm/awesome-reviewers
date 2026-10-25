---
title: Resilient failure recovery
description: 'Design UI/async code so it fails safely, cleans up deterministically,
  and recovers when the environment changes.


  Apply these rules:

  1) Gate irreversible transitions on success'
repository: CLINE/CLINE
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70837
---

Design UI/async code so it fails safely, cleans up deterministically, and recovers when the environment changes.

Apply these rules:
1) Gate irreversible transitions on success
- If a failure should leave the system usable, do not perform “detach/delete/sever” until the succeeding operation is confirmed.
- Example pattern:
  ```ts
  const { detach } = cloud;

  async function resume(sessionId: string) {
    try {
      // Resume local state first; only then detach cloud.
      await restoreLocalSession(sessionId);
      detach();
    } catch (e) {
      // On failure, keep cloud attached so user can retry.
      throw e;
    }
  }
  ```

2) Make cleanup robust to missing events
- Don’t assume `pointerup`, `visibilitychange`, etc. will always fire.
- Detect “stale drag” / “no button held” / “component unmounted” and run the same teardown path.

3) Implement explicit retry points tied to reconnection/environment changes
- For external-service lookups at startup, retry based on transport state changes (e.g., sidecar reconnect), not only on initial mount.
- Add a test for “first attempt fails, later reconnect succeeds.”

If you consistently (a) sequence side effects after success, (b) self-terminate when events don’t arrive, and (c) retry on reconnection, the codebase will handle real-world failure scenarios gracefully.