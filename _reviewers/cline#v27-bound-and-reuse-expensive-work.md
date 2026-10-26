---
title: Bound And Reuse Expensive Work
description: 'When code needs expensive IO/CPU (git queries, remote enumeration, terminal/clipboard
  capture, remote session hydration), avoid unnecessary fan-out and duplicate re-computation:'
repository: cline/cline#v27
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 70892
---

When code needs expensive IO/CPU (git queries, remote enumeration, terminal/clipboard capture, remote session hydration), avoid unnecessary fan-out and duplicate re-computation:

- Bound scope: don’t enumerate all remote state (e.g., all branch heads) when only a small subset is needed; prefer default/upstream branches or local tracking refs, and do the rest only after user confirmation.
- Batch and aggregate: when inspecting many files/objects, prefer one git process (e.g., `ls-tree` + `cat-file --batch`) rather than spawning `git show` per file.
- Reuse results: capture an expensive snapshot once and reuse it for both user-visible output and telemetry/success evaluation—never call the capture function twice.

Example pattern (reuse a single terminal snapshot for both telemetry and decision):
```ts
const terminalSnapshot = await getLatestTerminalOutput();
telemetryService.captureTerminalOutputFailure(terminalSnapshot.ok ? null : reason);
await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
```

Apply this standard anywhere you see repeated calls around the same expensive operation (capture/telemetry, preflight checks, hydration) or broad “list everything” git/remote queries before the user commits. The goal is fewer processes, fewer remote calls, lower latency, and less side-effect duplication.