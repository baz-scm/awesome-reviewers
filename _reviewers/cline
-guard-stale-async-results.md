---
title: Guard stale async results
description: Async operations (fetches, refreshes, clipboard reads, repository lookups)
  can resolve out of order or after the state they were meant to update has already
  moved on. Writing their results blindly causes stale data to overwrite newer state
  (an old account fetch landing after sign-out, a slow directory listing overwriting
  a fresh one, a late branch lookup...
repository: "cline/cline\r\n"
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70946
---

Async operations (fetches, refreshes, clipboard reads, repository lookups) can resolve out of order or after the state they were meant to update has already moved on. Writing their results blindly causes stale data to overwrite newer state (an old account fetch landing after sign-out, a slow directory listing overwriting a fresh one, a late branch lookup reverting a user's newer choice).

Apply these rules:

1. **Tag every async operation with a generation/request token captured before the `await`.** Increment the counter whenever a newer operation starts or whenever an event invalidates in-flight work (sign-out, explicit refresh, cache clear). After the `await`, compare the captured token to the current counter before performing any state write; if it no longer matches, discard the result silently.

```ts
const requestIdRef = useRef(0);

async function refresh() {
  const requestId = ++requestIdRef.current;
  const result = await fetchData();
  if (requestId !== requestIdRef.current) {
    return; // superseded by a newer call
  }
  setState(result);
}
```

   Scope the token to the smallest unit that can race independently (e.g. per-path, per-session) rather than a single global counter when multiple concurrent operations must be tracked separately.

2. **Prefer removing the race entirely over patching around it.** When state is being written from multiple async sources, consider moving to a single source of truth that resolves on every read/render instead of being computed and cached by the async caller — this avoids needing generation checks at all.

3. **Use an in-flight guard (not just a generation check) when an operation must not run concurrently with itself**, e.g. duplicate submits from rapid double-clicks or repeated paste shortcuts. Share one guard across all trigger paths that can start the same operation, set it before the async call, and release it after settling (with a short cooldown if needed to absorb rapid repeat triggers).

4. **Don't add synchronization that can't actually close the race window.** If a confirmation read is inherently a snapshot-in-time and a later external change can still invalidate it, re-reading or double-checking doesn't help — document why the existing single read is sufficient instead of adding false-safety code.

Always write a test that starts a newer operation, resolves the older one after it, and asserts the stale result was dropped.
</description>
