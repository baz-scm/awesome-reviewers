---
title: Race-safe concurrent state
description: 'Code that spans multiple await points or acts on shared/long-lived state
  (sessions, locks, lifecycle refs, worktrees, caches) must never trust a snapshot
  taken before the suspension point, and must never assume a status flag alone stops
  concurrent work. Two concrete rules follow from the recurring bugs:'
repository: can1357/oh-my-pi
label: Concurrency
language: TypeScript
comments_count: 19
repository_stars: 37317
---

Code that spans multiple await points or acts on shared/long-lived state (sessions, locks, lifecycle refs, worktrees, caches) must never trust a snapshot taken before the suspension point, and must never assume a status flag alone stops concurrent work. Two concrete rules follow from the recurring bugs:

1. **Re-verify identity/ownership right before you act, don't rely on an earlier read.** If a value can change while you `await` (a session id, the active persona, whether discovery finished, an agent ref's lifecycle, a lock/worktree owner), either read it through a live getter/accessor at the point of use, or capture an explicit identity (object reference, generation id, owner id) up front and compare-and-swap against it before mutating. Setting a terminal status (`aborted`, `parked`) is not enough — clear any TTL/timer/subscription that could still act on the old ref, and check "is this still *my* ref" before writing results back, deleting a file, or restoring a branch. Prefer atomic constructs (`fs.linkSync`/rename-based exclusive writes, compare-and-swap helpers, exact-reference equality) over "read, decide, write" sequences that leave a window for another async actor to intervene.

```ts
// Bad: snapshot taken before await, used to make a decision after it
const existing = this.#store.lookup(key); // sync read
if (existing) return this.#publish(key, baseUrl, existing);

// Good: re-check ownership/identity at the point you commit
const current = await this.#store.lookup(key);
if (current && current.ownerId === myOwnerId) return this.#publish(key, baseUrl, current);
```

2. **Bound every wait with a real deadline, and make the deadline actually stop the work**, not just stop *your* wait on it. Race the result against the deadline (`Promise.race`) instead of `await`-ing the operation's own completion signal — a killed process can still hold a pipe open via a surviving descendant, so the deadline must kill the whole process group / cancel pending readers, and your code must return at the deadline even if the underlying operation never settles. Route this kind of bounded, cancellable work through one shared helper instead of re-implementing spawn+timeout+kill at each call site.

Apply the same discipline to cancellation: an abort signal must be threaded through the *entire* chain of nested async work (hooks, subprocess trees, lifecycle timers, in-flight subscriber callbacks) so that aborting actually frees locks, processes, and files, rather than merely marking a status and leaving orphaned work running underneath.