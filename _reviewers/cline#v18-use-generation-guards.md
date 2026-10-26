---
title: Use generation guards
description: When async work can finish out of order (polls, user navigation, sign-out,
  refreshes, delayed reads), never let a late response blindly write state. Use a
  generation/version token to ensure only the newest request’s result is applied.
repository: cline/cline#v18
label: Concurrency
language: TSX
comments_count: 8
repository_stars: 70884
---

When async work can finish out of order (polls, user navigation, sign-out, refreshes, delayed reads), never let a late response blindly write state. Use a generation/version token to ensure only the newest request’s result is applied.

Standard:
1) Create a generation token per “scope” (component-wide, per key/path/id).
   - Example: a ref holding an integer counter (or a Map of counters by key).
2) Increment/assign the token when starting a new async request.
3) After every await (and before any state write), compare the current token with the latest one.
   - If it doesn’t match, drop the result.
4) If you keep cached UI while new snapshots arrive, mark entries stale and/or schedule a single follow-up read rather than letting older in-flight reads overwrite fresh data.
5) For side effects that can be triggered repeatedly (clipboard reads, double-clicks), add an in-flight guard so the second trigger returns early.
6) For hide/unmount lifecycle, ensure timers/flags used for async scheduling are cancelled and reset on cleanup so restoring the UI re-arms the needed work.

Code sketch:

```ts
const genRef = useRef(0);
const [state, setState] = useState<State>();

async function refresh() {
  const gen = ++genRef.current;
  const result = await api.getSomething();
  if (gen !== genRef.current) return; // drop stale response
  setState(result);
}

// Per key/path:
const keyGenRef = useRef(new Map<string, number>());
function invalidate(keys: string[]) {
  for (const k of keys) {
    keyGenRef.current.set(k, (keyGenRef.current.get(k) ?? 0) + 1);
  }
}
async function readKey(k: string) {
  const gen = (keyGenRef.current.get(k) ?? 0);
  const result = await api.read(k);
  if (gen !== (keyGenRef.current.get(k) ?? 0)) return; // dropped
  // safe write here
}
```

Apply this anywhere user intent (selection, auth state, visibility, refresh) can change while an async operation is in flight—especially in polling-driven UIs and component lifecycles.