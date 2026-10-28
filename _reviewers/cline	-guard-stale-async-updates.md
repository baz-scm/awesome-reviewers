---
title: Guard stale async updates
description: Hooks that perform async work (fetches, invokes, sends) tied to a specific
  session, thread, or request must guard against applying results after that context
  has changed—due to unmount, remount, rebind, or the user navigating away and back.
  Relying on a local ref/state captured at call time is unsafe because a retired hook
  instance's ref can still be...
repository: "cline/cline\t"
label: React
language: TypeScript
comments_count: 4
repository_stars: 70947
---

Hooks that perform async work (fetches, invokes, sends) tied to a specific session, thread, or request must guard against applying results after that context has changed—due to unmount, remount, rebind, or the user navigating away and back. Relying on a local ref/state captured at call time is unsafe because a retired hook instance's ref can still be mutated or read after its async call resolves, silently overwriting newer state (e.g., a failed send from pane A overwriting pane B's current draft).

Apply one of these patterns:
- Increment a generation/request counter before starting async work, capture it in a closure, and discard the result if the counter has changed by the time it resolves.
- Include all state that affects correctness (e.g., turn/user-message counts, not just tool-call counts) in the key used to validate "is this result still current," so staleness can't be masked by a key that didn't change when it should have.
- Before using a ref to decide behavior after an `await`, re-validate against the current/live identity (current thread ID, bound session ID) rather than trusting the instance's own ref, since that instance may already be retired.

Example pattern from a session-changes hook:

```ts
const requestRef = useRef(0);

useEffect(() => {
  const request = ++requestRef.current;
  fetchChanges().then((result) => {
    if (request === requestRef.current) {
      setResult(result); // only apply if still the latest request
    }
  });
}, [deps]);
```

And for identity-bound actions (e.g., per-session invoke/send), bump a `generationRef` on every rebind and check it before dispatching the reply, so a reply to an earlier binding is never applied to the current one. This prevents subtle bugs like duplicate messages, lost drafts, or stale "current" flags that are hard to reproduce without deliberately racing navigation against slow async operations.