---
title: Atomic Reservation And Recheck
description: 'When adding concurrency behavior (locks, in-flight guards, timeouts,
  retries, sampling), ensure three properties:


  1) Atomic “check-and-act” before any await (avoid TOCTOU)'
repository: QwenLM/qwen-code
label: Concurrency
language: TypeScript
comments_count: 7
repository_stars: 26407
---

When adding concurrency behavior (locks, in-flight guards, timeouts, retries, sampling), ensure three properties:

1) Atomic “check-and-act” before any await (avoid TOCTOU)
- Never do “check” in one async region and “act” after unrelated awaits unless the check and the reservation are made in one synchronous critical section.
- If you must reserve, do it with a synchronous check-and-add and ensure cleanup runs in the same control flow (typically `finally`).

2) Revalidate decisions against a fresh snapshot (avoid stale-snapshot races)
- If you sample facts (e.g., PR head) and then perform a multi-step async operation (pagination, per-item work), re-sample or re-check at the end and mark drift/fail-closed when facts no longer match.
- When a “re-read” guard exists, add tests that exercise the branch where the re-read changes the decision.

3) Cleanup must drain/await in-flight work even on failure (avoid teardown ordering bugs)
- In pipelines, if you accumulate async writes, always await/drain them in `finally` (or explicitly cancel them) so teardown (mode restore, session finalize) can’t occur while writes are still pending.

Practical patterns

A) Atomic in-flight reservation
```ts
const inFlight = new Set<string>();

async function createSession(id: string) {
  // synchronous check-and-add before any await
  if (inFlight.has(id)) throw new Error('409 conflict');
  inFlight.add(id);
  try {
    // do awaits/spawn here
    await doWork();
  } finally {
    inFlight.delete(id);
  }
}
```

B) Generation guard for out-of-order async completion
```ts
let gen = 0;
const lastApplied = { current: -1 };

async function refresh() {
  const myGen = ++gen;
  const value = await compute();
  if (myGen !== gen) return;         // stale completion
  if (lastApplied.current !== myGen) {
    lastApplied.current = myGen;
    setState(value);
  }
}
```

C) Double-sample + drift flag
```ts
const headBefore = await getPrHead();
const comments = await fetchAllComments();
const headAfter = await getPrHead();
const drift = headBefore !== headAfter;
// If drift, mark threads as staleWorktree or fail-closed.
```

D) Drain async writes in finally
```ts
let outputWrites = Promise.resolve();

try {
  await pumpInputToPty();
  await outputWrites;
  return;
} finally {
  // ensure pending writes finish or are cancelled before teardown
  await outputWrites.catch(() => {});
}
```

If any change touches session creation, process spawning, locks/reservations, per-attempt retries, terminal/IO pipelines, or sampling across async boundaries, apply this checklist and add regression tests for the “race-changed-decision” branches—not just the happy path.