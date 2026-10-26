---
title: Avoid redundant heavy work
description: When code performs expensive operations (subprocesses, remote Git/network
  calls, clipboard/capture, or session rehydration), make sure you (a) do it once
  per user action and (b) do the minimum necessary fan-out. Also, only apply timeouts
  that match real streaming behavior.
repository: cline/cline#v3
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70863
---

When code performs expensive operations (subprocesses, remote Git/network calls, clipboard/capture, or session rehydration), make sure you (a) do it once per user action and (b) do the minimum necessary fan-out. Also, only apply timeouts that match real streaming behavior.

Practical rules:
1) Reuse already-captured data
- If a function already fetches a snapshot (terminal output, model payload, git stdout), don’t fetch it again for telemetry or branching logic.

2) Reduce subprocess/IO fan-out
- Prefer batching (e.g., `git cat-file --batch`) over per-file/per-blob `git show` loops.
- Before running remote discovery (e.g., listing heads/commits), scope it to the required default/upstream branch or use local refs instead of downloading everything.

3) Avoid background side effects during hydration
- Don’t automatically connect/rehydrate remote resources in UI/sidebar hydration unless the user explicitly opened that data.

4) Timeouts must match streaming semantics
- Ensure “first chunk” timeouts only apply when you can reasonably expect streamed deltas; otherwise long “thinking” (no deltas) can be incorrectly aborted.

Example patterns:
- Deduplicate expensive capture:
```ts
async function fallbackCaptureWithTelemetry() {
  const snapshot = await getLatestTerminalOutput(); // capture once
  telemetryService.captureTerminalOutputFailure(/* reason */, snapshot);
  returnCurrentTerminalContentsFromSnapshot(snapshot); // reuse
}
```
- Batch Git blob reads instead of per-file subprocesses:
```ts
const child = execFile('git', ['-C', cwd, 'cat-file', '--batch'], {/*...*/});
child.child.stdin?.end([...new Set(oids)].join('\n') + '\n');
// parse stdout once; skip large blobs before reading them
```
- Limit remote head listing:
```ts
// Instead of ls-remote --heads <remote>, prefer default/upstream only
const headSha = await git(root, ['rev-parse', '@{u}']); // or query a single known ref
```

Applying these checks during review will directly prevent latency spikes, unnecessary CPU/memory pressure, and costly background network/proc activity—core performance risks highlighted by the discussions.