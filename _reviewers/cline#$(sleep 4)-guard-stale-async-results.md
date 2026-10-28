---
title: Guard stale async results
description: 'A huge fraction of concurrency bugs in this codebase share one shape:
  code captures some state, starts an `await`, and then — without re-checking whether
  the world changed while it was suspended — uses the result to mutate shared state,
  resolve a promise, or release a resource. Any value, lock, or identity read before
  an `await` must be treated as...'
repository: cline/cline#$(sleep 4)
label: Concurrency
language: TypeScript
comments_count: 18
repository_stars: 70978
---

A huge fraction of concurrency bugs in this codebase share one shape: code captures some state, starts an `await`, and then — without re-checking whether the world changed while it was suspended — uses the result to mutate shared state, resolve a promise, or release a resource. Any value, lock, or identity read before an `await` must be treated as provisionally stale once control returns.

Apply these three guards wherever an async operation's result will be applied back to shared/mutable state:

1. **Stamp and re-check an identity/generation token.** Before starting async work, record the current "generation" (a bind id, epoch, revision, importId, reason-generation, etc.) of the thing you're about to act on. After the `await`, compare it again before applying the result; if it moved on, drop the stale result instead of applying it.
   ```ts
   const generation = ++this.generation;
   const result = await doWork();
   if (generation !== this.generation) return; // superseded; discard
   this.apply(result);
   ```
   This pattern recurs for reconnect/rebind logic, revision-gated UI actions, rebuild schedulers keyed by reason, and status caches refreshed from a live connection.

2. **Claim ownership synchronously, before the first `await`, when a shared resolver/slot/record could otherwise be grabbed twice.** Don't gate on a callback or `isCurrent()` flag that is only checked *after* the async step — that still leaves a window where two callers both pass the check. Take the resolve function, delete the pending-start record, or null out the slot immediately, then do the async work with the local copy.
   ```ts
   const resolve = this.pendingResolve
   if (!resolve) return false
   this.pendingResolve = undefined // claimed; no other caller can resolve this now
   await deliverAttachments()
   resolve(text)
   ```
   Only forget/release a provisional resource (e.g. a "pending start" record) once the async operation has observably taken effect (the sandbox accepted the turn), not merely once it was launched.

3. **Use compare-and-swap, not unconditional writes, when releasing or replacing a shared slot (map entry, session resident, cache host).** A `finally`/cleanup block must check that the slot still points at *this* instance before deleting or disposing it, otherwise it can tear down a concurrently-installed replacement.
   ```ts
   if (this.sessions.get(id) === residentBeforeRebuild) {
     this.sessions.delete(id); // only if nothing replaced it meanwhile
   }
   ```
   The same principle applies to "pin while in use" counters (don't dispose a host another in-flight operation is actively using) and to serializing writes to the same resource through a chained promise queue so a late write can't land on top of a newer one.

When you find yourself patching a fifth similar stale-state window with another ad hoc flag or reset, that's a signal to invert the design instead: record the authoritative value synchronously at the point of decision (e.g., set-and-throw in the same tick) rather than trying to reconcile it after the fact from multiple racing callbacks.