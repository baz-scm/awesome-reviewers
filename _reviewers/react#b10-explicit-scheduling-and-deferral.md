---
title: Explicit Scheduling and Deferral
description: 'When writing concurrent code, make execution order and deferral strategy
  explicit—don’t rely on implicit synchronicity.


  Guidelines:

  1. Keep controlled input updates synchronous; defer expensive derived computations
  to transition/deferral priority.'
repository: facebook/react#b10
label: Concurrency
language: JavaScript
comments_count: 7
repository_stars: 251894
---

When writing concurrent code, make execution order and deferral strategy explicit—don’t rely on implicit synchronicity.

Guidelines:
1. Keep controlled input updates synchronous; defer expensive derived computations to transition/deferral priority.
2. Implement `scheduleMicrotask`/`scheduleWork` as true scheduling primitives. Use a host-appropriate microtask mechanism (`queueMicrotask` when available). If you must fall back, do it via a Promise microtask and ensure errors surface reliably.
3. If a platform requires synchronous scheduling (e.g. `renderToString`), isolate that exception and leave a clear TODO/notes to revisit.
4. In tests, avoid timing races: use `act`/`actAsync` (or an equivalent) so assertions run after the intended async work.

Example (browser-like microtask scheduling with safe fallback):

```js
function handleErrorInNextTick(error) {
  setTimeout(() => { throw error; });
}

export const scheduleMicrotask =
  typeof queueMicrotask === 'function'
    ? queueMicrotask
    : callback => {
        Promise.resolve(null).then(callback).catch(handleErrorInNextTick);
      };
```

Example (synchronous input, deferred derived search):

```js
const [searchText, setSearchText] = useState('');
const deferredText = useDeferredValue(searchText);

const searchResults = useMemo(
  () => findMatches(deferredText),
  [deferredText]
);

function onChange(next) {
  setSearchText(next); // sync input update
}
```
