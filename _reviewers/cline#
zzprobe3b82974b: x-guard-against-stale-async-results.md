---
title: Guard against stale async results
description: Async operations (network fetches, polling, clipboard reads, sandbox/session
  creation) can complete out of order when a newer trigger (a retry, a cancel, a navigation,
  a user re-triggering the same action) fires before an earlier one settles. If the
  earlier result is applied unconditionally, it silently overwrites newer, correct
  state — e.g. a stale...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 71067
---

Async operations (network fetches, polling, clipboard reads, sandbox/session creation) can complete out of order when a newer trigger (a retry, a cancel, a navigation, a user re-triggering the same action) fires before an earlier one settles. If the earlier result is applied unconditionally, it silently overwrites newer, correct state — e.g. a stale repository list replacing a fresh one, or a cloud session created before a `/clear` reattaching itself after the clear.

Guard every async write-back with a generation/request-id check:
1. Capture a ref/counter snapshot (or bump it) before starting the async call.
2. After the `await`, compare the captured value against the current counter; only apply the result if nothing newer has started/invalidated it.
3. On any action that invalidates in-flight work (reset, clear, cancel), bump the counter so pending completions become no-ops instead of being hard-cancelled — this lets slow operations finish harmlessly rather than being killed outright.

```ts
const requestRef = useRef(0);
async function refresh() {
  const id = ++requestRef.current;
  const result = await fetchSomething();
  if (id !== requestRef.current) return; // superseded, drop it
  applyResult(result);
}
```

When the same race can be eliminated by design, prefer that over adding more guards: make the client state a pure read-only derivation of a single source of truth (e.g. resolve the server-authoritative value on every render) instead of writing it from multiple async call sites.

Separately, for handlers that can be re-entered concurrently (double-click, repeated Ctrl+V, rapid taps), add an in-flight guard that short-circuits while a previous call is still pending, rather than relying on generation counters alone — this prevents duplicate side effects (e.g. clipboard text pasted twice).