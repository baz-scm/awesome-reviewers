---
title: Guard against stale async races
description: 'Whenever a long-running or asynchronous operation (a network call, a
  planner invocation, a file read, a session rebuild, a connection attempt) can overlap
  with a newer event, request, or state change, the code must not let a stale result
  silently overwrite or act on behalf of current state. Two complementary techniques
  should be applied together as needed:'
repository: 'cline/cline

  '
label: Concurrency
language: TypeScript
comments_count: 18
repository_stars: 70942
---

Whenever a long-running or asynchronous operation (a network call, a planner invocation, a file read, a session rebuild, a connection attempt) can overlap with a newer event, request, or state change, the code must not let a stale result silently overwrite or act on behalf of current state. Two complementary techniques should be applied together as needed:

1. Claim shared mutable state synchronously, before the first `await`. If a resolver, lock, or pending-request slot will be consumed by an async step, capture and clear it immediately so a second caller cannot race in and act on the same slot. For example:
```ts
const resolve = this.pendingAskResolve
if (!resolve) return false
this.pendingAskResolve = undefined // later submissions route as follow-ups
await deliverAttachments()
resolve(responseText)
```
Delaying the claim until after an await (e.g. `await deliverAttachments(() => this.pendingAskResolve === resolve)`) leaves a window where a second event can observe and consume the same pending state before the first one finishes.

2. Tag in-flight work with a generation/version/epoch and validate it on resume. Before applying the result of an async operation, check that nothing newer has superseded it (a newer run started, the session was replaced, the bind/scope changed, the plugin was reloaded, a newer request for the same reason arrived). Increment a counter or stamp an identity object at the point a newer operation begins, and have every deferred continuation check that stamp before mutating shared state, pushing UI updates, or releasing a resource:
```ts
const generation = this.generation
const result = await doWork()
if (generation !== this.generation) return // superseded; discard
this.apply(result)
```
This pattern should be used for: resolving promises/callbacks, applying fetched or computed state, releasing/disposing resources that a replacement may already own, and deciding whether to retry or skip in-flight requests. When releasing or disposing a resource that another operation may have already replaced, re-check identity immediately before the destructive action (e.g. `if (this.sessions.get(id) === resident) release(resident)`), not just at the start of the async function.

Favor these checks over ad hoc flags that are reset at some later point (e.g. only in a `cancel()` method); a self-contained generation check at the point of resuming is far less likely to leave a window where stale work is misattributed to current state.