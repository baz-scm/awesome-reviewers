---
title: UseEffect Dependency Correctness
description: 'Side effects must be written with the correct React lifecycle mental
  model: `useEffect` runs after render/commit, not at the place the code is written.
  Always include a dependency array and make the effect’s inputs explicit so state
  resets (e.g., initializing defaults when a dialog opens) happen at the right time
  and without stale reads.'
repository: infiniflow/ragflow
label: React
language: TSX
comments_count: 4
repository_stars: 80174
---

Side effects must be written with the correct React lifecycle mental model: `useEffect` runs after render/commit, not at the place the code is written. Always include a dependency array and make the effect’s inputs explicit so state resets (e.g., initializing defaults when a dialog opens) happen at the right time and without stale reads.

Apply this standard:
- If logic depends on props/state (e.g., `visible`, `defaultValues`, `formCallbackRef`), include them in the `useEffect` dependency list.
- Perform “reset when dialog opens” inside an effect keyed to the open/visible flag rather than relying on render-order.

Example (dialog reset):
```ts
useEffect(() => {
  const initialDeleteValue = chunk_num > 0;
  setDefaultValues({ delete: initialDeleteValue, apply_kb: false });

  if (visible && formCallbackRef.current) {
    formCallbackRef.current.reset({ delete: initialDeleteValue, apply_kb: false });
  }
}, [visible, chunk_num, setDefaultValues]);
```

Also: extract repeated side-effect logic into hooks when appropriate (to avoid duplicated effect code), but keep each hook’s effect dependencies correct.