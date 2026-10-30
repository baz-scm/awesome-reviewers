---
title: Guard stale async responses
description: 'Whenever an async operation (fetch, refresh, clipboard read, cloud session
  create) can be re-triggered before the previous call resolves, its result must not
  be allowed to silently overwrite state with stale data or fire duplicate side effects.
  Apply one of these patterns:'
repository: cline/cline#"><b>zze3729958
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 71067
---

Whenever an async operation (fetch, refresh, clipboard read, cloud session create) can be re-triggered before the previous call resolves, its result must not be allowed to silently overwrite state with stale data or fire duplicate side effects. Apply one of these patterns:

1. **Generation/request counters**: capture a monotonically increasing token (per-key when multiple concurrent targets exist, e.g. per directory path) before starting the async call, and after every `await` compare it to the current token before writing any state. Discard the result if a newer call has since started. Example:
```ts
const requestId = ++requestRef.current;
const result = await fetchSomething();
if (requestId !== requestRef.current) return; // stale, drop it
setState(result);
```
This must be checked immediately before *every* state write that follows an `await`, not just the first one — intermediate awaits can also be overtaken.

2. **In-flight guards**: when an action can be triggered twice in quick succession (double-click, repeated keypress, overlapping submits), use a ref-based "pending" flag that short-circuits re-entrancy and is released only after the operation settles (optionally with a short cooldown). Do not add this guard to paths that are already synchronous/non-racy (e.g., inline paste events that carry data directly, with no async read) — only guard the paths that actually perform an async operation.

3. **Prefer removing the race by construction** over patching individual races: store only the authoritative user intent/state synchronously, and treat async lookups (e.g., validating a branch name against a remote) as pure reads that resolve derived state rather than as writes that can race with a later user action. Read the "current" value through a ref at the moment of writing (not a value captured in a stale closure) so a write that follows an await reflects the latest state, not what was true when the async call started.

When reviewing concurrent/async code, check: (a) can this call be re-triggered before it resolves, (b) is every post-await state write guarded against staleness, and (c) would restructuring state ownership eliminate the race entirely rather than requiring a guard. Add a test that starts a second call, lets the first one resolve late, and asserts the stale result had no effect.