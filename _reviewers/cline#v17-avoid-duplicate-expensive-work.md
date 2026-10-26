---
title: Avoid Duplicate Expensive Work
description: When code needs an expensive I/O/compute step (clipboard capture, git
  remote inspection, filesystem scanning, etc.), ensure it’s done (a) at most once
  per decision point and (b) with the smallest required scope.
repository: cline/cline#v17
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 70883
---

When code needs an expensive I/O/compute step (clipboard capture, git remote inspection, filesystem scanning, etc.), ensure it’s done (a) at most once per decision point and (b) with the smallest required scope.

Apply two checks:
1) Reuse captured/derived values
- If you already fetched a snapshot/derived output for the main control-flow, reuse that same value for telemetry, success/failure messages, and later decisions—don’t re-run the capture.

Example (pattern):
```ts
async function fallbackWithTelemetry(telemetryService: any) {
  // Do the expensive capture once
  const terminalSnapshot = await getLatestTerminalOutput();

  // Use it for both messaging and telemetry
  telemetryService.captureTerminalOutputFailure(/* reason */ "TIMEOUT");
  emitFallbackMessageFrom(terminalSnapshot);
}
```

2) Bound remote/IO discovery
- For git/network discovery, don’t enumerate everything (e.g., all remote heads) if you only need one logical target (default/upstream branch) or if local refs are sufficient.

Example (pattern):
```ts
// Instead of listing every remote head SHA, inspect only the upstream/default branch.
const defaultBranch = "origin/main"; // or resolved upstream/default
const sha = await git(root, ["rev-parse", defaultBranch]);
```

This standard reduces latency, avoids duplicated side effects, lowers bandwidth/history downloads, and prevents telemetry/message divergence from multiple independent captures.