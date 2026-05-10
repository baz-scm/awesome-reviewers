---
title: Concurrency-safe async flows
description: 'When UI actions can occur rapidly or in parallel (double-clicks, retries,
  rapid test submissions), treat them as concurrency problems: synchronize the triggering
  and centralize the side effects.'
repository: freeCodeCamp/freeCodeCamp
label: Concurrency
language: TSX
comments_count: 3
repository_stars: 444449
---

When UI actions can occur rapidly or in parallel (double-clicks, retries, rapid test submissions), treat them as concurrency problems: synchronize the triggering and centralize the side effects.

Apply two rules:
1) Guard “repeatable” actions (submit/reset/etc.) with stable synchronization and cleanup.
- Don’t inline-create debounced/locked functions in a way that changes across re-renders—this can weaken protection.
- Use a stable ref for the dispatch target and debounce it once; cancel pending debounced work on unmount.

```ts
const SUBMIT_DEBOUNCE_MS = 1000;

export function useSubmit() {
  const dispatch = useDispatch();

  const submitRef = useRef(() => dispatch(submitChallenge()));
  submitRef.current = () => dispatch(submitChallenge());

  const debouncedSubmitRef = useRef(
    debounce(() => submitRef.current(), SUBMIT_DEBOUNCE_MS, {
      leading: true,
      trailing: false,
    })
  );

  useEffect(() => {
    const debouncedSubmit = debouncedSubmitRef.current;
    return () => debouncedSubmit.cancel();
  }, []);

  return () => debouncedSubmitRef.current();
}
```

2) Centralize API + store mutation in a single orchestrator (e.g., saga).
- UI components should pass “intent” (what to delete/reset/submit) rather than directly mixing API calls with store updates.
- This reduces inconsistent state transitions and race conditions (including special responses like 204 where store updates may otherwise be skipped).

Result: fewer race-condition bugs, more deterministic behavior under fast user input and automated rapid submissions, and clearer ownership of async workflows.