---
title: Bound parallel async lifecycle
description: 'For any async workflow that fans out (e.g., Promise.all over providers)
  or mutates shared session state, apply two rules:

  1) Bound/cancel all external async work (timeouts must abort the underlying operation,
  not only the awaiting caller).'
repository: aaif-goose/goose
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 51876
---

For any async workflow that fans out (e.g., Promise.all over providers) or mutates shared session state, apply two rules:
1) Bound/cancel all external async work (timeouts must abort the underlying operation, not only the awaiting caller).
2) Centralize lifecycle transitions for shared mutable state (prefer a state enum + transition helper over ad-hoc “reset fields in parallel”).

How to apply
- Concurrency bounding: wrap each provider call with a timeout and ensure the server/backend uses an equivalent timeout that cancels/drops the in-flight fetch/subprocess.
- State transitions: introduce a lifecycle enum (e.g., PromptLifecycle) and a single function that sets all related fields together when transitioning states, rather than resetting individual fields scattered across code paths.

Example (client-side timeout with defense-in-depth)
```ts
const LIVE_MODELS_TIMEOUT_MS = 4000;

function withTimeout<T>(promise: Promise<T>, ms: number, label: string): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`${label} timed out after ${ms}ms`)), ms);
    promise.then(
      (value) => { clearTimeout(timer); resolve(value); },
      (err) => { clearTimeout(timer); reject(err); }
    );
  });
}

// In fan-out code, ensure each task is bounded so Promise.all can complete.
const liveIds = await withTimeout(
  acpListProviderSupportedModels(providerId),
  LIVE_MODELS_TIMEOUT_MS,
  `live model discovery for ${providerId}`
);
```

Example (lifecycle state centralized)
```ts
enum PromptLifecycle { Idle, AwaitingRun, Running, Succeeded, Failed }

function transitionEntry(entry: Entry, next: PromptLifecycle) {
  // Reset/updates happen in one place to keep concurrent transitions consistent.
  switch (next) {
    case PromptLifecycle.Idle:
      entry.activePromptAttemptId = null;
      entry.activeRunId = null;
      return;
    // other states...
  }
}
```

This prevents: (a) UI workflows stalling indefinitely due to a single slow dependency, (b) leaked in-flight work when only the client await is timed out, and (c) inconsistent session state caused by partial or parallel field resets.