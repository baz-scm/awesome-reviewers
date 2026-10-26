---
title: Guard Async Races
description: Treat any async operation whose result may arrive out of order as potentially
  stale. Before writing to React state (or other shared state), prove the response
  is still current.
repository: cline/cline#v7
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70865
---

Treat any async operation whose result may arrive out of order as potentially stale. Before writing to React state (or other shared state), prove the response is still current.

Apply these rules:
- Add a generation/token guard for each “resource key” (e.g., runtime, directory path, account/org). Increment it when starting a new request or when invalidating (refresh, sign-out, selection change). After every await, compare the token; if it doesn’t match, return without state writes.
- If multiple user events can trigger the same async side effect (e.g., clipboard reads), use an in-flight guard/ref so only one read appends/commits.
- Prefer “canonical input + derived resolution” over writing derived target/state from async results. If state can be recomputed from current sources, don’t persist derived fields in the async callback.
- Ensure lifecycle hide/unmount cleanup resets timers/flags that would otherwise prevent correct re-arming or re-entry after remount.

Example (generation guard pattern):
```ts
const genRef = useRef(0);
const [state, setState] = useState<Data | undefined>();

async function refresh() {
  const myGen = ++genRef.current;
  const result = await api.fetchData();
  if (myGen !== genRef.current) return; // stale
  setState(result);
}

function invalidate() {
  genRef.current++; // e.g., sign out / selection changed
}
```

If you adopt this consistently, you prevent stale requests from overwriting newer state, avoid duplicate async side effects, and eliminate whole classes of race-condition UI/data corruption.