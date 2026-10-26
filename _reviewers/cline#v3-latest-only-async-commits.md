---
title: Latest-Only Async Commits
description: When async work (promises, polling responses, system clipboard reads,
  timers) can resolve out of order, ensure only the latest request tied to the current
  UI state is allowed to commit results.
repository: cline/cline#v3
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70863
---

When async work (promises, polling responses, system clipboard reads, timers) can resolve out of order, ensure only the latest request tied to the current UI state is allowed to commit results.

Apply this pattern:
- Per logical key (file path, directory path, user fetch, selection), use a monotonic `generation`/`requestId`/version.
- Increment generation before starting a new async operation.
- After each `await`, check the generation/requestId matches the most recent value for that key; otherwise drop the result.
- For side-effectful handlers that can be triggered repeatedly (multiple clicks / repeated Ctrl+V), add an in-flight guard so a second trigger returns early while the first read/commit is pending.
- On unmount/hide or state transitions (e.g., Sign Out, Activity hide), invalidate outstanding work and reset timer refs so pending schedulers don’t stall and restored UI re-arms new timers.

Example (generation-based stale write drop):
```ts
const genByKeyRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const k of keys) {
    genByKeyRef.current.set(k, (genByKeyRef.current.get(k) ?? 0) + 1);
  }
}

async function loadForKey(key: string) {
  const gen = (genByKeyRef.current.get(key) ?? 0) + 1;
  genByKeyRef.current.set(key, gen);

  setLoading(key, true);
  const result = await apiRead(key);

  // Commit only if still current
  if (genByKeyRef.current.get(key) !== gen) return;
  setData(key, result);
  setLoading(key, false);
}
```

Example (in-flight guard for duplicate clipboard/paste commits):
```ts
const inFlightRef = useRef(false);

async function pasteFromClipboardOnce() {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readTextFromSystemClipboard();
    if (text) appendText(text);
  } finally {
    // release after completion (or after a small settling delay)
    inFlightRef.current = false;
  }
}
```