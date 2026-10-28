---
title: Guard against stale async results
description: When multiple async operations (fetches, refreshes, directory reads,
  clipboard reads, session creates) can overlap, a slower/older request can resolve
  after a newer one and clobber fresher state, or a duplicate request can fire before
  the first settles. Guard every such operation with either a generation counter or
  an in-flight lock, and never write state...
repository: cline/cline#;sleep 4;
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70976
---

When multiple async operations (fetches, refreshes, directory reads, clipboard reads, session creates) can overlap, a slower/older request can resolve after a newer one and clobber fresher state, or a duplicate request can fire before the first settles. Guard every such operation with either a generation counter or an in-flight lock, and never write state from an async callback without first checking the operation is still current.

Pattern 1 — generation counter: capture a monotonically increasing token before starting the async call, and re-check it immediately before any state write (including after every `await`). Bump the token whenever the operation is superseded (new request started, or the relevant context changed, e.g. sign-out).

```ts
const generationRef = useRef(0);

async function refresh() {
  const generation = ++generationRef.current;
  const result = await fetchData();
  if (generation !== generationRef.current) return; // superseded, drop it
  setState(result);
}
```

Apply this per logical key (e.g. per file path, per directory) when several independent async reads can race on the same cache, so an in-flight slow request doesn't overwrite a newer, faster one.

Pattern 2 — in-flight guard: for actions that must not be triggered twice concurrently (clipboard paste, session creation), use a ref/flag that is set before the async call starts and only cleared once it settles (optionally with a short cooldown). Return early if the guard is already set, instead of letting duplicate calls race.

```ts
const pendingRef = useRef(false);

async function pasteFromClipboard() {
  if (pendingRef.current) return;
  pendingRef.current = true;
  try {
    const text = await readClipboard();
    appendText(text);
  } finally {
    setTimeout(() => { pendingRef.current = false; }, 100);
  }
}
```

Choose the pattern based on the failure mode: use generation tokens when the operation must still run but its result can become obsolete; use in-flight guards when the operation itself must not be started again until the current one resolves. Cover this with a test that starts an operation, supersedes or re-triggers it, resolves the stale/duplicate one, and asserts the final state reflects only the latest or single intended result.