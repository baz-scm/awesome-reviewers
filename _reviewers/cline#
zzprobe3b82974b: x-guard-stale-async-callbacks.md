---
title: Guard stale async callbacks
description: Hooks that kick off async work (invokes, promises, event subscriptions)
  must not blindly apply the result when it finally resolves. By the time it lands,
  the component may have unmounted, remounted for a different thread/session, started
  a newer run, or the user may have changed the draft/attachments. Several bugs in
  this codebase came from exactly this...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: React
language: TypeScript
comments_count: 6
repository_stars: 71067
---

Hooks that kick off async work (invokes, promises, event subscriptions) must not blindly apply the result when it finally resolves. By the time it lands, the component may have unmounted, remounted for a different thread/session, started a newer run, or the user may have changed the draft/attachments. Several bugs in this codebase came from exactly this pattern: a late reply from a stale run overwriting fresher state, a retired pane's `handleSend` continuation clobbering a newer draft in a shared Map, an "Undo" that assumed success instead of checking what was actually removed, and a one-key Send using the file list captured before the wait instead of reconciling it against what's still attached when the verdict arrives.

To avoid this class of bug:
- Give every bind/run/session a stable identity (a generation counter, run id, or revision) and capture it before starting the async call.
- Before applying the async result to state, refs, or shared external stores (e.g. a cross-pane `Map<threadId, draft>`), check that the identity captured at call time still matches the current one. If it doesn't, discard the result.
- When the result's success depends on current state (e.g. "was this file still attached?", "was this prompt actually removed?"), snapshot what's needed at call time and re-derive the real outcome from what the async call actually reports, not from assumptions.
- Don't key shared caches only by a value that can be reassigned to multiple logical identities (e.g. a thread id that can alias to two sessions); validate/migrate aliases explicitly.

Example pattern:
```ts
const generationRef = useRef(0);

async function run(sessionId: string) {
  generationRef.current += 1;
  const generation = generationRef.current;
  const result = await invoke(sessionId, action);
  if (generation !== generationRef.current) return; // stale, discard
  applyResult(result);
}
```

Apply the same discipline to effect cleanup and subscriptions: treat any callback whose side effects target state outside its own render cycle as needing an explicit staleness/identity check before it mutates anything.