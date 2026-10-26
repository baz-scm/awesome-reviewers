---
title: Reuse Expensive Results
description: When code needs an expensive IO/network/process result (git output, terminal
  snapshot, remote discovery), compute it once and reuse it—don’t re-capture/re-run
  the same expensive operation for telemetry, success/failure checks, or UI hydration.
  Also batch or constrain discovery calls so you don’t do per-item work or fetch unneeded
  data.
repository: cline/cline#v6
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70864
---

When code needs an expensive IO/network/process result (git output, terminal snapshot, remote discovery), compute it once and reuse it—don’t re-capture/re-run the same expensive operation for telemetry, success/failure checks, or UI hydration. Also batch or constrain discovery calls so you don’t do per-item work or fetch unneeded data.

Apply this by:
- **Capture once, reuse everywhere**: if a function already fetches a snapshot, return it (or pass it out) and use the same value for telemetry and downstream logic.
- **Avoid per-item process spawning**: replace loops of `git show`/`exec` with a single batched command (e.g., `git cat-file --batch`) when you need many blobs.
- **Gate remote work to user intent**: don’t rehydrate/open remote sessions during sidebar/background hydration; rely on cached/discovery metadata.
- **Constrain discovery enumeration**: listing “all remote heads” or branches can be costly—limit to the needed/default ref or local tracking where possible.

Example pattern (reuse a single terminal snapshot for both fallback and telemetry):
```ts
async function fallbackCaptureOnce() {
  const terminalSnapshot = await getLatestTerminalOutput(); // one expensive capture
  telemetryService.captureTerminalOutputFailure(
    terminalSnapshot ? TerminalOutputFailureReason.NONE : TerminalOutputFailureReason.TIMEOUT,
    { snapshotLen: terminalSnapshot.length },
  );
  await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
}
```

If you must enforce timeouts for performance, ensure the timeout applies to the right phase of streaming/processing (don’t abort long “thinking” phases just because no early tokens arrived).