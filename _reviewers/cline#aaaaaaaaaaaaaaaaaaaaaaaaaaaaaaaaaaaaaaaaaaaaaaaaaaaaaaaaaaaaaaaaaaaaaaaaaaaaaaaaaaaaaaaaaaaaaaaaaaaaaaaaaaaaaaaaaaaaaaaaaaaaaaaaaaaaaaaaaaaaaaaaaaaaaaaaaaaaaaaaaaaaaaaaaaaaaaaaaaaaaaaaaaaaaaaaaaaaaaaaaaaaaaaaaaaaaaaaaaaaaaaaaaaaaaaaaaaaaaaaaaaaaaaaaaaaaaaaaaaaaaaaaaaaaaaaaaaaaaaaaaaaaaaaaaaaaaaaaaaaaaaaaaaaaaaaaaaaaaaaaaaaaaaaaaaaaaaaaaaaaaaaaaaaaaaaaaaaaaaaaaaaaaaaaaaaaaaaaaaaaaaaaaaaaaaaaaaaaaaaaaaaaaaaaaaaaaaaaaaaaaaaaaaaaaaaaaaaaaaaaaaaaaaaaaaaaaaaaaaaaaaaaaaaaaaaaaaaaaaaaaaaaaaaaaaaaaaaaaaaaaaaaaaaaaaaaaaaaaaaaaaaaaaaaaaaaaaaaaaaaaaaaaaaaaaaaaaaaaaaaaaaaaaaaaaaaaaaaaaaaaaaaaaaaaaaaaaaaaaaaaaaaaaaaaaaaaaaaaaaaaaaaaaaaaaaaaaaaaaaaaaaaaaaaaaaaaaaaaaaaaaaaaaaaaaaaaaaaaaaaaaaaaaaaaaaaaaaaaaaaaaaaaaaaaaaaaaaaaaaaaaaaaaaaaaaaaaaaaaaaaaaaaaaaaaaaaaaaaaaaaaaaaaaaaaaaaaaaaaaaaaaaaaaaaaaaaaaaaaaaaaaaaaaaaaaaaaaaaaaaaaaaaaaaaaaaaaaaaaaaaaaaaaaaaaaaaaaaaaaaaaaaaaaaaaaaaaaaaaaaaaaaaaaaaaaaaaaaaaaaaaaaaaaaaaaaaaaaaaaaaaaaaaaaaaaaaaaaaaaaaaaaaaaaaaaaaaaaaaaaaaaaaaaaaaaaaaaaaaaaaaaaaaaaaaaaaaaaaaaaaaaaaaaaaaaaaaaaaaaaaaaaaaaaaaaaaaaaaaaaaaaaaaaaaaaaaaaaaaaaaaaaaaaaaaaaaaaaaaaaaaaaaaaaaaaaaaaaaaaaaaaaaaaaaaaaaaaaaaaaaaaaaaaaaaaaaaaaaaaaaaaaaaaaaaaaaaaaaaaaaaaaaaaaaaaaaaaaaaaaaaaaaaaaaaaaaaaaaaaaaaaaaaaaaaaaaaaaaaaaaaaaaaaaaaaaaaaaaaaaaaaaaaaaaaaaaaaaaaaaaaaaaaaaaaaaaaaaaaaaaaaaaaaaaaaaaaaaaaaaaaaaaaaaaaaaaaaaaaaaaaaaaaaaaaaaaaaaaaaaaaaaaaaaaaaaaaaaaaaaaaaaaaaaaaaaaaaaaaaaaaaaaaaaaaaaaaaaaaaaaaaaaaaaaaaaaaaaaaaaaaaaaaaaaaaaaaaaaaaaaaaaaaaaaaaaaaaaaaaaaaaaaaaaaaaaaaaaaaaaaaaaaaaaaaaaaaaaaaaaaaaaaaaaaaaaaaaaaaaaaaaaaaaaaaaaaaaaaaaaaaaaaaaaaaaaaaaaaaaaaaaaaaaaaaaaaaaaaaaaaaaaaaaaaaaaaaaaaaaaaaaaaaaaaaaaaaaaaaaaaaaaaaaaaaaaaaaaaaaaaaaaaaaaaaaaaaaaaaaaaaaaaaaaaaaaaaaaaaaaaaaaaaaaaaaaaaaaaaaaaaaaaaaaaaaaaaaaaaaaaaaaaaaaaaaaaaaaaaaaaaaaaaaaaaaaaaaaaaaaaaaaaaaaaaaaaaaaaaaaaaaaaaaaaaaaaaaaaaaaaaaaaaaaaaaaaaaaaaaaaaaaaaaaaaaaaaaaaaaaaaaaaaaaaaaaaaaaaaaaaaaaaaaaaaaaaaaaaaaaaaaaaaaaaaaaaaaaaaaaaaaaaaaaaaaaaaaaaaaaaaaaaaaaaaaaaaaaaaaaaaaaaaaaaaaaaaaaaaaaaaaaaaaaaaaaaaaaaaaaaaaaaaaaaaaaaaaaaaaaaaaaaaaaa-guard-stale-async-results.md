---
title: Guard stale async results
description: 'Many of these hooks kick off async work (invoking a backend verb, awaiting
  a promise, racing a timeout) whose result is applied later to shared refs, component
  state, or a dispatcher. Between the start and the resolution of that async call,
  the relevant context can change: the component can unmount/remount (e.g. navigating
  away and back to a thread), the...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TypeScript
comments_count: 6
repository_stars: 70967
---

Many of these hooks kick off async work (invoking a backend verb, awaiting a promise, racing a timeout) whose result is applied later to shared refs, component state, or a dispatcher. Between the start and the resolution of that async call, the relevant context can change: the component can unmount/remount (e.g. navigating away and back to a thread), the bound session/thread can switch, a generation of state can be superseded, or the user can edit the draft/attachments again. If the async callback blindly applies its result to "current" state without re-validating that context, it produces races: a retired pane's failed send overwrites a newer draft, a stale `attach`/`invoke` reply gets applied to the wrong session, a one-key Send ships files that were removed while waiting for its verdict, or an optimistic UI update gets misplaced relative to a concurrently-arriving message.

Standard: whenever a hook starts an async operation that will later touch shared or external state, capture a generation token, identity (session/thread id), or a snapshot of the relevant data at dispatch time, and re-validate it against the current value before applying the result. If the context no longer matches, discard the result (or reconcile explicitly) instead of writing it through.

```ts
const generation = ++generationRef.current;
const boundSessionId = sessionId;
const result = await invoke(action);
if (generation !== generationRef.current || boundRef.current !== boundSessionId) {
  return; // stale reply from a superseded bind/instance — ignore it
}
dispatch({ type: "reply", result });
```

Apply the same discipline to:
- Refs/maps shared across remounts (e.g. draft caches) — validate the owning instance/thread is still current before writing back after an awaited call.
- Verb handlers awaiting a server verdict — re-check the bound session/revision/generation before dispatching the result, and snapshot any mutable inputs (attached files, draft text) at the moment the action fires rather than reading them again when the verdict lands.
- Derived booleans/state computed from multiple independent async streams (partial vs. acknowledged updates, optimistic vs. persisted messages) — make ordering/filtering explicit instead of assuming a fixed arrival order.

This prevents hard-to-reproduce race conditions and keeps UI state consistent with the operation the user actually triggered.