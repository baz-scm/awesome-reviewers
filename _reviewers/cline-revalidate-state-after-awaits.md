---
title: Revalidate state after awaits
description: 'Many races in this codebase come from code that reads shared mutable
  state (a session slot, a cached config, an in-flight "current" pointer, a pending
  promise resolver), then awaits something, and finally acts on a stale assumption
  that nothing changed in the meantime. Examples: a teardown writing a session''s
  terminal status after a replacement already took...'
repository: cline/cline
label: Concurrency
language: TypeScript
comments_count: 15
repository_stars: 70886
---

Many races in this codebase come from code that reads shared mutable state (a session slot, a cached config, an in-flight "current" pointer, a pending promise resolver), then awaits something, and finally acts on a stale assumption that nothing changed in the meantime. Examples: a teardown writing a session's terminal status after a replacement already took over the slot; a turn dispatched onto a runtime that a concurrent rebuild has since replaced; a planner serving a set built from an environment snapshot that predates a branch switch; a pending "ask" resolver being claimed by two concurrent answers; a UI action referencing a tray/offer revision that a newer set already superseded.

To avoid this class of bug:
1. **Snapshot inputs before the first await**, not after, when a decision depends on "what the caller saw" (e.g. the model shown in a composer, the resolver being claimed). Claim/capture synchronously, before yielding control, so a concurrent caller cannot interleave.
2. **Re-validate after every await** before performing a side effect that is visible outside the local scope (writing status, deleting a slot, resolving a promise, applying a UI update). Use an explicit "is this still current" check — a generation/revision counter, an object-identity comparison (`this.sessions.get(id) !== resident`), or a "displaced" predicate — and re-check it right before the side effect, not just once at entry.
3. **Prefer building the replacement before tearing down the original** so there is never a window where the shared slot is empty or inconsistent; only release/overwrite the old state once it has been safely displaced.
4. **Serialize conflicting writes** to the same resource (a per-key promise chain, a mutex, or a "superseded" queue) rather than relying on whichever async write happens to finish last.

Example pattern used to fix several of these races:
```ts
const generation = this.scopeGeneration; // snapshot before awaiting
const result = await doAsyncWork();
if (this.disposed || generation !== this.scopeGeneration) {
  // superseded while we were awaiting — do not apply side effects
  return;
}
this.apply(result);
```
Apply this discipline anywhere an async function can be re-entered or raced by another caller touching the same session, cache entry, file, or UI state, and add a regression test that starts the race (hold one operation mid-await, trigger the competing one, then release) to pin the expected outcome.