---
title: Graceful error handling
description: 'When handling failures in UI/async flows, design for graceful degradation
  and predictable recovery:


  - Treat async outcomes as explicit states (uninitialized/loading/loaded/failed).
  Never let “empty success” be conflated with “not fetched,” and avoid recursive re-fetch
  loops.'
repository: microsoft/VSCode
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 194303
---

When handling failures in UI/async flows, design for graceful degradation and predictable recovery:

- Treat async outcomes as explicit states (uninitialized/loading/loaded/failed). Never let “empty success” be conflated with “not fetched,” and avoid recursive re-fetch loops.
- For non-critical optional capabilities, use best-effort behavior: catch RPC/config lookup failures, log a warning, and keep the primary workflow running.
- Preserve user-facing invariants during errors (e.g., focus, visible/selected surface), and make recovery deterministic (retry/fallback paths should restore the right pending state).
- Ensure cleanup and diagnostics always run: use try/finally to dispose resources and capture logs, even if closing/teardown throws.
- Validate inputs defensively before coercion/processing (e.g., handle NaN and out-of-bounds early) so errors are consistent and don’t cascade.

Example (pattern):
```ts
type SnapshotState = 'uninitialized' | 'loading' | 'loaded' | 'failed';

let state: SnapshotState = 'uninitialized';

async function ensureSnapshot() {
  if (state !== 'uninitialized') return; // don't loop on empty success
  state = 'loading';
  try {
    const result = await queryMarketplaceSnapshot();
    // empty array is still a terminal loaded-success
    render(result);
    state = 'loaded';
  } catch (e) {
    state = 'failed';
    showRetryUI();
    // focus Retry/error so recovery is usable
    focusRetry();
  }
}

async function optionalCapability() {
  try {
    return await rpc.getBuiltinDescriptors({});
  } catch (e) {
    logService.warn('Optional capability unavailable; continuing with defaults', e);
    return undefined; // fail open
  }
}

async function runWithCleanup() {
  const accessor = services.createTestingAccessor();
  try {
    return await work(accessor);
  } finally {
    accessor.dispose();
    captureLogsIfNeeded();
  }
}
```

Adopting this approach prevents the most painful failure modes seen in the discussions: infinite re-render/request loops, core workflows breaking due to auxiliary RPC failures, broken UX recovery (like lost focus), and missing cleanup/log capture during failures.