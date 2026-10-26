---
title: Guard async state commits
description: 'When async work can overlap (multiple refreshes, navigations, sign-out,
  queued reads, clipboard/paste), never write results back to state unless the result
  still matches the latest intent. Use one of:'
repository: cline/cline?x=1
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70861
---

When async work can overlap (multiple refreshes, navigations, sign-out, queued reads, clipboard/paste), never write results back to state unless the result still matches the latest intent. Use one of:

- Generation/version tokens per request (global or per-key) checked after every await.
- Single-flight/in-flight guards for operations where duplicates are harmful (e.g., clipboard read).
- If possible, restructure so derived state is computed from current canonical inputs (store minimal user intent; resolve derived values on state updates), making stale commits impossible.

Example (generation per key/request):
```ts
const generationRef = useRef(new Map<string, number>());

const invalidate = (key: string) => {
  generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
};

async function loadThing(key: string) {
  const requestGen = (generationRef.current.get(key) ?? 0) + 1;
  generationRef.current.set(key, requestGen);

  const result = await fetchThing(key);

  // Commit only if still current
  if ((generationRef.current.get(key) ?? 0) !== requestGen) return;
  setState(result);
}
```

Example (single-flight paste/read to prevent duplicates):
```ts
const inFlightRef = useRef(false);

async function pasteFromClipboardOnce() {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readTextFromSystemClipboard();
    if (text) append(text);
  } finally {
    setTimeout(() => { inFlightRef.current = false; }, 100);
  }
}
```

Standard expectation: any `await` followed by state writes must either be protected by a generation/in-flight guard or be proven impossible to race with newer user intent.