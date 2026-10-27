---
title: Low-Overhead Performance Patterns
description: 'Prefer low-allocation, non-blocking patterns in hot paths and UI-critical
  code.


  Do:

  - Replace allocation-heavy loops (e.g., `apply` chunking/subarrays) with native
  decoders or streaming-friendly APIs, and keep guarantees (like bijective mappings)
  explicit.'
repository: facebook/react#b4
label: Performance Optimization
language: JavaScript
comments_count: 8
repository_stars: 251885
---

Prefer low-allocation, non-blocking patterns in hot paths and UI-critical code.

Do:
- Replace allocation-heavy loops (e.g., `apply` chunking/subarrays) with native decoders or streaming-friendly APIs, and keep guarantees (like bijective mappings) explicit.
- Avoid per-iteration closures/helper allocations; hoist reusable functions and only allocate in the branch that truly needs it.
- Guard before calling expensive logic so most inputs never enter large parsing/dispatch functions.
- Avoid recursion growth in paths that can fan out to many listeners; check state and proceed without deep recursive calls.
- Defer expensive derived computations (tree walks, large searches) so they don’t block controlled input updates; optionally show a “pending” indicator.
- If you introduce continuation/tiling/splitting logic, watch for worst-case tail slicing and repeated retained work; prefer index-based continuation over repeated `slice`/tail allocations.
- For correctness/perf-sensitive changes, benchmark and keep the change isolated; GC-based tests should be robust to non-determinism.

Example (defer expensive work + show pending):
```js
const [text, setText] = useState('');
const deferredText = useDeferredValue(text);
const matches = useMemo(() => computeMatches(deferredText), [deferredText]);

const pending = text !== deferredText;
return (
  <input value={text} onChange={e => setText(e.target.value)} />
  {pending ? <Spinner/> : <Results list={matches} />}
);
```

Example (avoid recursion fan-out):
```js
// Instead of recursively calling wakeChunkIfInitialized(...),
// prefer checking status and then performing the correct wake/reject action.
if (status === 'initialized') wakeChunk(chunk);
else if (status === 'errored') rejectChunk(chunk, reason);
```

This standard reduces GC pressure, prevents accidental stack/hidden-class deopts, and keeps the UI responsive under load.