---
title: Guard against async races
description: 'Async operations (clipboard reads, network creates, file/directory listings,
  state-confirmation reads) can overlap, resolve out of order, or be triggered twice
  by independent UI paths. Protect against this with two complementary patterns:'
repository: cline/cline#&&sleep 4
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70980
---

Async operations (clipboard reads, network creates, file/directory listings, state-confirmation reads) can overlap, resolve out of order, or be triggered twice by independent UI paths. Protect against this with two complementary patterns:

1. **In-flight guards for duplicate triggers.** When the same async action can be started from multiple entry points (e.g. a keyboard shortcut and a mouse click, or two rapid submits), use a single shared ref/promise to dedupe concurrent calls instead of letting each path race independently. Example: unify mouse-paste and Ctrl+V paste behind one `pasteFromClipboard` call that returns early while a read is pending.

2. **Generation/version tokens to discard stale results.** When an async operation's result is applied to shared state, capture a generation counter or request-identity object before starting the async work, and only apply the result if that token is still current when it resolves. Bump/replace the token whenever the owning state is reset or superseded (e.g. on `/clear`, a newer poll, or a newer write). This prevents a slow or delayed response from reattaching to or clobbering state that has since moved on.

```ts
const generationRef = useRef(0);

async function refresh(key: string) {
  const generation = ++generationRef.current;
  const result = await fetchSomething(key);
  if (generationRef.current !== generation) return; // stale, discard
  applyResult(result);
}
```

Apply this pattern anywhere a value can be reset, reassigned, or superseded while an async call tied to the old value is still in flight — session creation, polling/listing, clipboard reads, and confirmation re-reads after a write. When confirming the outcome of a concurrent write, prefer re-reading authoritative state over assuming success/failure locally, since partial failures (e.g. a write succeeding before a dependent step fails) make local assumptions unreliable.