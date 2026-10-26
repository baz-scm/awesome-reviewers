---
title: Minimize Expensive Work
description: Prefer designs that (1) do only the work you truly need, (2) deduplicate
  repeated work, and (3) batch external/process-heavy operations—especially before
  user confirmation.
repository: cline/cline#v29
label: Performance Optimization
language: TypeScript
comments_count: 8
repository_stars: 70893
---

Prefer designs that (1) do only the work you truly need, (2) deduplicate repeated work, and (3) batch external/process-heavy operations—especially before user confirmation.

Practical guidelines:
- Scope network/git enumeration: don’t fetch “everything” (e.g., all remote heads) unless required for the current step.
- Batch process calls: avoid per-file/per-item `git` subprocess spawning; use single-invocation batch mechanisms when possible.
- Reuse computed results: if you already fetched/derived a snapshot for output/UI/telemetry, pass/reuse it instead of fetching again.
- Gate high-frequency UI state changes: ensure conditional logic doesn’t cause unnecessary show/hide churn during partial streaming/hand-offs.
- Use timeouts that match real behavior: “first chunk” timers can abort legitimate long-thinking runs if no early stream events occur—apply stricter timers only when appropriate.

Example: reuse a single terminal snapshot for both emitted fallback and success telemetry (avoid duplicate clipboard capture):
```ts
async function captureWithFallback() {
  // Fetch once
  const terminalSnapshot = await getLatestTerminalOutput();

  // Emit fallback based on the same snapshot
  const fallbackMsg = makeFallbackMessage(terminalSnapshot);
  emitFallback(fallbackMsg);

  // Telemetry should reuse the same snapshot (not re-fetch)
  telemetryService.captureTerminalOutputSuccess({ snapshot: terminalSnapshot });
}
```

Example: batch git blob reads instead of spawning one `git show` per file:
```ts
async function readBlobsBatch(cwd: string, oids: Iterable<string>) {
  const unique = [...new Set(oids)];
  if (!unique.length) return new Map<string, string>();

  const pending = execFile('git', ['-C', cwd, 'cat-file', '--batch'], {
    windowsHide: true,
    maxBuffer: Number.POSITIVE_INFINITY,
    encoding: 'buffer',
  });

  pending.child.stdin?.end(unique.join('\n') + '\n');
  const { stdout } = await pending;
  // parse stdout once here...
  return new Map();
}
```

Checklist to apply in reviews:
- “Is this step doing full-repo/network enumeration when only a subset is needed?”
- “Are we spawning external processes per item, when batching is available?”
- “Did we compute something once and then accidentally fetch/recompute it again?”
- “Could a timeout/guard cause avoidable aborts and retries for valid slow operations?”