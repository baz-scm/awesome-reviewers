---
title: Guard async state races
description: Hooks that combine optimistic UI updates with async confirmations (debounced
  state, deferred promises, streamed partial messages) are prone to race conditions
  across timing gaps and component lifecycle transitions (unmount/remount, navigation
  away and back). Before writing or rendering based on an async result, validate it
  against the current state/identity...
repository: cline/cline
label: React
language: TypeScript
comments_count: 3
repository_stars: 70886
---

Hooks that combine optimistic UI updates with async confirmations (debounced state, deferred promises, streamed partial messages) are prone to race conditions across timing gaps and component lifecycle transitions (unmount/remount, navigation away and back). Before writing or rendering based on an async result, validate it against the current state/identity rather than trusting a stale ref, closure, or an incomplete combined condition:

- When composing boolean visibility/state conditions from multiple async-derived flags, make sure a more specific state (e.g. a provisioning/loading marker) actually suppresses the others in the combined expression, not just in an internal helper that isn't wired into the final condition.
- When reconciling an optimistic entry with incoming async messages (e.g. searching backward to replace a placeholder), account for all message kinds that can be interleaved, so unrelated async arrivals don't break the match and cause duplicates.
- For async callbacks that originate from a component instance that may have been unmounted/remounted (e.g. draft text tied to a thread, replaced after navigating away and back), check the callback against the current version/identity of the target before applying its result; never let a retired instance's ref overwrite newer state just because its promise resolves late.

Example pattern — validate identity/version before applying a late async result:
```ts
const handleSend = async (threadId: string, version: number) => {
  try {
    await sendPrompt(threadId);
  } catch {
    if (isCurrent(threadId, version)) {
      restoreDraft(threadId, promptInputRef.current);
    }
    // else: thread was remounted/navigated away; drop the stale write
  }
};
```

Additionally, cover these races with tests that exercise the full hook (not just a pure helper) across the relevant lifecycle sequence — e.g. mount → async event → unmount → remount → late resolution — asserting the final state is correct.