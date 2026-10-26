---
title: Avoid redundant async
description: 'Treat performance regressions as “wasted work” and “unbounded resources.”
  Apply these rules:


  - Reuse already-computed results: if a helper already fetched data (e.g., terminal
  output snapshot), do not fetch again for telemetry/UI—derive all outputs from the
  same snapshot.'
repository: cline/cline#v7
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70865
---

Treat performance regressions as “wasted work” and “unbounded resources.” Apply these rules:

- Reuse already-computed results: if a helper already fetched data (e.g., terminal output snapshot), do not fetch again for telemetry/UI—derive all outputs from the same snapshot.

  ```ts
  async function fallbackWithTelemetry() {
    const terminalSnapshot = await getLatestTerminalOutput(); // single capture
    telemetryService.captureTerminalOutputFailureReasonedFrom(terminalSnapshot);
    await returnSnapshotToModel(terminalSnapshot);
  }
  ```

- Avoid eager fan-out before confirmation: don’t prefetch large/expensive remote data (e.g., all remote heads) when only a subset is needed for the current step. Prefer limiting to default/upstream branches or lightweight local refs.

- Batch and bound external IO:
  - Batch per-file Git operations into a single process when many entries exist.
  - Enforce hard size limits on downloads/archives and stop reading/cancel once over the limit.

  ```ts
  // Prefer one batch process over N per-file calls
  const input = [...new Set(oids)].join("\n");
  const { stdout } = await execFile("git", ["-C", cwd, "cat-file", "--batch"], { input });
  ```

- Clean up immediately on early settlement (timeouts/fallbacks): when you resolve/reject early, ensure you drop inherited stdio pipes/listeners and clear timers so background children can’t keep the host alive or keep writing.

- Add tests that catch performance/resource bugs: e.g., verify active pipe handles don’t grow after fallback settlement, and verify loader/side-effect churn doesn’t occur for partial provisioning states.

This standard prevents the common causes shown here: duplicate expensive captures, unnecessary network/history downloads, uncontrolled process/memory growth, and lingering stdio/resource leaks.