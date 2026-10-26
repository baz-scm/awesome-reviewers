---
title: Reuse expensive results
description: When code needs an expensive result (process output, git/remote data,
  clipboard/terminal snapshots, remote session hydration, etc.), compute it once and
  reuse it—especially in fallback paths, telemetry paths, and validation/preflight
  layers. Avoid re-invoking the same heavy operation just to emit a metric or build
  another message, and avoid broad...
repository: cline/cline#v15
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 70877
---

When code needs an expensive result (process output, git/remote data, clipboard/terminal snapshots, remote session hydration, etc.), compute it once and reuse it—especially in fallback paths, telemetry paths, and validation/preflight layers. Avoid re-invoking the same heavy operation just to emit a metric or build another message, and avoid broad enumeration that multiplies work (e.g., all remote heads) when only a scoped answer is required.

Apply these rules:
- If a function already captures data for correctness/UI, return that snapshot and reuse it for telemetry/logging.
- Remove duplicated checks/loops executed in the same control flow.
- Ensure heavy repo/remote preflight logic isn’t repeated across layers.
- Scope or batch remote/process work to the minimum necessary set (default branch/upstream; `git cat-file --batch` vs per-file `git show`).
- Gate background IO and UI churn during known transitional states (provisioning/hydration).
- Enforce hard size/time bounds and stop reading once limits are exceeded.

Example (dedupe snapshot + reuse for telemetry):
```ts
async function handleFallback() {
  // BAD: captures output twice
  // await returnCurrentTerminalContents();
  // telemetry.captureTerminalOutputFailure(await getLatestTerminalOutput());

  // GOOD: capture once, reuse everywhere
  const terminalSnapshot = await getLatestTerminalOutput();
  const fallbackMessage = buildFallbackMessage(terminalSnapshot);

  emitFallbackToModel(fallbackMessage);
  telemetry.captureTerminalOutputFailure({ snapshot: terminalSnapshot });
}
```