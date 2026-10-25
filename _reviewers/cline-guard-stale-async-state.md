---
title: Guard stale async state
description: When an async operation can be superseded (new request, sign-out, selection
  change, hide/show), never let its late response commit state unconditionally. Use
  a concurrency token (generation/requestId) and validate it right before every state
  write.
repository: cline/CLINE
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70839
---

When an async operation can be superseded (new request, sign-out, selection change, hide/show), never let its late response commit state unconditionally. Use a concurrency token (generation/requestId) and validate it right before every state write.

Apply this standard:
- **Generation / requestId per operation key**: increment a ref (globally or per path/item) before starting, and compare after every `await`.
- **Commit-time “still current?” checks**: before writing, verify the user/context selection is still the one that triggered the request (use a ref and/or an updater function that reads the latest selection).
- **Prevent duplicate side effects**: for async clipboard/system reads or similar, use an **in-flight guard** so repeated UI events can’t append twice.
- **Reset async schedulers on visibility transitions**: ensure timers/flags are fully cleared/reset when app state is hidden/shown so remounting doesn’t stall or double-schedule work.

Example (generation + commit guard):
```ts
const genRef = useRef(0);

async function refresh() {
  const gen = ++genRef.current;
  setLoading(true);
  try {
    const result = await desktopClient.invoke('some_call', {/*...*/});
    if (gen !== genRef.current) return; // superseded
    setData(result);
  } finally {
    if (gen === genRef.current) setLoading(false);
  }
}

// For selection-triggered async:
const selectionRef = useRef(selection);
selectionRef.current = selection;

async function lookupAndPossiblyWrite() {
  const captured = selectionRef.current;
  const result = await fetchSomething(captured);
  if (selectionRef.current !== captured) return; // selection changed
  setSelectionFromResult(result);
}
```

This prevents race conditions where older responses overwrite newer state, where sign-out/hide transitions leave stale writes behind, and where repeated triggers duplicate async effects.