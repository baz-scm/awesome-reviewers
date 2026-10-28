---
title: Revalidate state after awaits
description: 'Most concurrency bugs in these reviews share one shape: code resumes
  after an `await` and assumes the world is still as it was before that await — the
  session wasn''t replaced or torn down, the bind/scope/account wasn''t superseded,
  the item/row/connection it''s about to act on is still the current one. Any external
  event (teardown, restart, reload, cancel,...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Concurrency
language: TypeScript
comments_count: 28
repository_stars: 70965
---

Most concurrency bugs in these reviews share one shape: code resumes after an `await` and assumes the world is still as it was before that await — the session wasn't replaced or torn down, the bind/scope/account wasn't superseded, the item/row/connection it's about to act on is still the current one. Any external event (teardown, restart, reload, cancel, reconnect, detach, account switch) can land during the suspended gap, so acting on stale assumptions causes duplicate work, lost writes, leaked resources, or actions applied to the wrong target.

Apply two complementary techniques:

1. **Capture identity before the await, recheck immediately before the side effect.** Snapshot a generation counter, the current resident/object reference, or an abort/cancellation flag before starting the async work, then re-validate it right before the next mutation or terminal action — not just once at the top of the function, but after *every* await that could race with a supersession, since the window can reopen at each one:

```ts
const resident = this.sessions.get(sessionId);
const displaced = () => this.sessions.get(sessionId) !== resident;

await doSomeAsyncWork();
if (displaced()) return; // another start/teardown already took over

await doMoreAsyncWork();
if (displaced()) return; // re-check again; state can change between awaits too

this.sessions.set(sessionId, newState); // safe: still current
```

   This pattern (generation ids, `isCurrent()`/`displaced()` checks, bind generations, scope generations) should guard every reconnect retry, withdrawal, UI state publish, and teardown path that resumes after I/O.

2. **Serialize conflicting operations on the same resource instead of relying on last-write-wins.** When two operations (e.g., a status write and a teardown write, two account switches, two rebuild requests) can legitimately race, don't just check staleness — chain them on a shared promise/queue so they execute in a well-defined order and later ones see the effects of earlier ones:

```ts
private pending = Promise.resolve();
switchAccount(id?: string): Promise<void> {
  const next = this.pending.then(() => this.switchAccountNow(id), () => this.switchAccountNow(id));
  this.pending = next;
  return next;
}
```

Before shipping any code with an `await` followed by a mutation, ask: "what else could have changed while I was suspended, and did I re-check for it?" Add a regression test that holds the async step open (a deferred promise, a paused mock) and triggers the competing event during that window — this is how every fix referenced above was verified.