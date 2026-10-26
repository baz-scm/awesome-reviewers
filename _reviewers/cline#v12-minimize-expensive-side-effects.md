---
title: Minimize Expensive Side Effects
description: When code performs costly work (git/network/process/terminal capture)
  or runs fallback paths, ensure it does not (a) duplicate that work, (b) broaden
  the scope to full-history/entire-repo when not needed, or (c) leak resources that
  keep the host alive or trigger unintended background connections.
repository: cline/cline#v12
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70872
---

When code performs costly work (git/network/process/terminal capture) or runs fallback paths, ensure it does not (a) duplicate that work, (b) broaden the scope to full-history/entire-repo when not needed, or (c) leak resources that keep the host alive or trigger unintended background connections.

Apply this checklist:
- Reuse results: if a function already fetched a value (e.g., terminal output snapshot), don’t fetch again for telemetry/success checks—derive everything from the single capture.
- Bound expensive queries: avoid “all branches/heads” or full scans unless required; prefer default/upstream branches or local tracking refs.
- Batch/fan-in external operations: avoid per-file/per-item git or process spawning when a batch API exists.
- Clean up on fallback/settlement: when settling early, remove listeners and close/stop using inherited stdio so a background grandchild can’t keep the host alive or keep buffering output.
- Avoid background reconnection during UI hydration: only connect remotely when explicitly needed; rely on discovery/cached metadata otherwise.

Example (reuse capture result instead of recapturing):
```ts
const terminalSnapshot = await getLatestTerminalOutput();
const ok = terminalSnapshot.includes("...");
telemetryService.captureTerminalOutputFailure(ok ? undefined : reason, { terminalSnapshot });
await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
```

Example (batch git reads to reduce process fan-out):
```ts
const input = [...new Set(oids)].join("\n");
const { stdout } = await execFile("git", ["-C", cwd, "cat-file", "--batch"], { encoding: "buffer" });
// parse stdout to fill a map; avoid `git show ref:path` per file
```