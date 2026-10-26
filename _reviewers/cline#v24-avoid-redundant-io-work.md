---
title: Avoid redundant I/O work
description: 'When code needs data from Git/network/filesystem, ensure it’s not doing
  unnecessary repeated work and that it’s bounded.


  Apply these checks:

  - **Scope/limit enumeration**: don’t fetch “everything” (e.g., all remote heads)
  just to preview; restrict to upstream/default or use local refs.'
repository: cline/cline#v24
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70891
---

When code needs data from Git/network/filesystem, ensure it’s not doing unnecessary repeated work and that it’s bounded.

Apply these checks:
- **Scope/limit enumeration**: don’t fetch “everything” (e.g., all remote heads) just to preview; restrict to upstream/default or use local refs.
- **Batch expensive subprocesses**: replace per-file `git show`/process-per-item patterns with batched commands (e.g., `git cat-file --batch`) to reduce host load.
- **Hard cap resources**: enforce max bytes and cancel/stop reading as soon as the cap is exceeded; prefer incremental reads over “buffer the whole response”.
- **Compute once, reuse**: if you already captured a snapshot/result for telemetry/UI, reuse it—don’t call the capture function again (especially if it triggers clipboard/side effects).
- **No background connects on hydration**: avoid initiating remote session/Hub connections during UI hydration when it can be deferred until the user opens the session.

Example pattern (reuse computed snapshot to avoid duplicate capture):
```ts
const snapshot = await getLatestTerminalOutput();
telemetryService.captureTerminalOutputFailure(
  /* reason */ timeoutReason,
  /* success */ snapshot.trim().length > 0,
  /* message */ snapshot,
);
```