---
title: Guard async hook state
description: 'Hooks that kick off async work (invoking a backend verb, fetching data,
  waiting on a debounced acknowledgement) must defend against the world changing before
  the result lands. Several bugs in this codebase came from reading "live" refs or
  recomputing derived state after an `await` instead of trusting what was true when
  the action started:'
repository: "cline/cline\r\n"
label: React
language: TypeScript
comments_count: 6
repository_stars: 70946
---

Hooks that kick off async work (invoking a backend verb, fetching data, waiting on a debounced acknowledgement) must defend against the world changing before the result lands. Several bugs in this codebase came from reading "live" refs or recomputing derived state after an `await` instead of trusting what was true when the action started:

- **Snapshot the inputs you'll need, not just the result.** If an action's correctness depends on state that can mutate while awaiting (e.g. which files are attached, which message was the "sent" one), capture that state into a snapshot at the moment the action fires, and use the snapshot afterward — don't re-read the live ref.
- **Guard against stale replies with a generation/bind counter.** Before awaiting, capture a generation id (or the bound session/target). After the await resolves, compare against the current generation/binding before dispatching or mutating state; discard the reply if they no longer match.
- **Make "is this still current" checks depend on everything that invalidates it.** A memoized/fetched value's freshness key must include every input that can make a previous fetch stale (e.g. include message/turn counters in a refresh key, not just a subset), otherwise an async result from an earlier state can be mistaken for current.
- **Never call a hook conditionally to suppress its effect.** Push the gating condition into the value passed to the hook (e.g. `!cloudProvisioning && (optimisticShow || ...)`), keep the hook call unconditional, and cover the combined condition with a full-hook test rather than only the extracted helper.
- **When reconciling optimistic UI with confirmed state, filter out unrelated interleaved entries** instead of relying on positional/backward search, so an intervening system message doesn't cause duplicate or mismatched entries.

Example pattern for guarding async replies:

```ts
const generationRef = useRef(0);

async function runAction(targetId: string) {
  const generation = ++generationRef.current;
  const snapshot = captureRelevantState(); // e.g. attached files, draft, etc.
  const result = await invoke(targetId, snapshot);
  if (generation !== generationRef.current) return; // stale, discard
  applyResult(result, snapshot);
}
```

Apply this discipline to any hook performing async verbs, debounced fetches, or optimistic updates so stale results can't overwrite newer state.