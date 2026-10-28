---
title: Guard stale async results
description: 'Hooks frequently kick off asynchronous work (an invoke, a debounced
  fetch, a verdict wait) while other state keeps changing. Treat every such gap as
  a race and defend against it explicitly:'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: React
language: TypeScript
comments_count: 5
repository_stars: 70984
---

Hooks frequently kick off asynchronous work (an invoke, a debounced fetch, a verdict wait) while other state keeps changing. Treat every such gap as a race and defend against it explicitly:

- Snapshot the inputs you need at the moment the operation starts (e.g., the attached files, the bound session/request id) instead of re-reading live refs once the result arrives, since the live value may have moved on.
- Guard every async callback with an identity/version check before applying its result — compare a request counter, a bound-session id, or similar (`if (request !== requestRef.current) return;` / `if (boundRef.current !== boundSessionId) return;`). This prevents an outdated response from overwriting newer state or re-inserting stale UI (e.g., duplicate messages, previous-turn data).
- When a key decides whether a result is "current" (a refresh key, cache key, dependency array), make sure it encodes every input that affects correctness. A partial proxy — e.g., a key that changes only on tool calls but not on new user messages — will let a stale result be treated as current.
- Never make a hook call itself conditional. Compute the gating boolean from the async/optimistic state and pass it into the hook's arguments or the value it evaluates, rather than branching around the hook invocation.

Example pattern for guarding a debounced/async fetch:

```ts
const requestRef = useRef(0);
useEffect(() => {
  if (!enabled) return;
  const request = ++requestRef.current;
  const timer = setTimeout(() => {
    fetchData(params).then((result) => {
      if (request === requestRef.current) setResult({ key: refreshKey, result });
    });
  }, DEBOUNCE_MS);
  return () => clearTimeout(timer);
}, [enabled, refreshKey, ...params]);
```

Applying this consistently avoids the class of bugs seen when a one-key send captures stale file lists, a session-changes hook reports stale data as "current", a loader flickers because a hook call was conditionally skipped, or an async warning/message gets duplicated because the merge logic didn't account for concurrent state changes.</description>
</invoke>
