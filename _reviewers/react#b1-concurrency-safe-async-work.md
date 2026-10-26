---
title: Concurrency-safe async work
description: 'When adding async/concurrent behavior, make updates responsive and keep
  scheduling + invariants correct across suspension and nesting.


  **Standards**

  1) **Don’t block user input with expensive work**: keep controlled/input state updates
  synchronous; compute expensive/derived results at transition/deferred priority.'
repository: facebook/react#b1
label: Concurrency
language: JavaScript
comments_count: 8
repository_stars: 251878
---

When adding async/concurrent behavior, make updates responsive and keep scheduling + invariants correct across suspension and nesting.

**Standards**
1) **Don’t block user input with expensive work**: keep controlled/input state updates synchronous; compute expensive/derived results at transition/deferred priority.
2) **Be explicit about scheduling semantics**: if you implement `scheduleMicrotask`, use native `queueMicrotask` when available; otherwise use a Promise-based microtask shim with proper error surfacing.
3) **Preserve invariants across suspend/re-entrancy**: if code uses mutable shared variables or performs destructive rendering that may suspend, restore previous values and don’t move “push/pop” logic across potential suspend points.
4) **Avoid never-resolving async resources**: don’t create promises that can remain pending forever—prefer `Promise.resolve()` or properly resolved/rejected promises so the system can progress.

**Example (responsive input + deferred derived search)**
```js
const [searchText, setSearchTextState] = useState('');
const deferredText = useDeferredValue(searchText);

// Controlled update stays synchronous
const onChange = (text) => setSearchTextState(text);

// Derived computation runs at transition priority
const matches = useMemo(() => {
  if (deferredText === '') return [];
  return findMatches(deferredText); // expensive tree walk
}, [deferredText]);
```

**Example (microtask scheduling fallback)**
```js
function handleErrorInNextTick(error) {
  setTimeout(() => { throw error; });
}

const scheduleMicrotask =
  typeof queueMicrotask === 'function'
    ? queueMicrotask
    : (cb) => {
        Promise.resolve(null).then(cb).catch(handleErrorInNextTick);
      };
```

Apply these checks during review: “Could this block interactive updates?”, “Does scheduling match across platforms?”, “What happens if this suspends or is nested—are we restoring state / keeping push-pop ordering?”, and “Can this async work ever stall forever?”