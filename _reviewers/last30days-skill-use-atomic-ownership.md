---
title: Use Atomic Ownership
description: When coordinating concurrent work (threads or processes), make “ownership”
  explicit and authoritative, and ensure every consumer uses the same claimed/produced
  result.
repository: mvanhorn/last30days-skill
label: Concurrency
language: Python
comments_count: 2
repository_stars: 57799
---

When coordinating concurrent work (threads or processes), make “ownership” explicit and authoritative, and ensure every consumer uses the same claimed/produced result.

Apply this in two common patterns:

1) Coalesce duplicate in-flight work (threads)
- Use a shared gate that (a) lets exactly one “leader” perform the work and (b) forces all “waiters” to block until the leader publishes the final outcome.
- Don’t invent speculative errors (e.g., synthetic early timeouts) while the leader is still viable.
- Ensure the leader’s publish/finish step is idempotent so failure-safety nets can’t overwrite a successful result.

Example pattern (simplified):
```python
with lock:
    cached = cache.get(key)
    if cached is not None:
        return copy.deepcopy(cached)
    inflight = inflight_map.get(key)
    if inflight is not None:
        event = inflight.event
        slot = inflight.slot
        # waiter: block for the leader’s publish
    else:
        event = threading.Event()
        slot = [None]
        inflight_map[key] = (event, slot)
        # leader: run work, then finish

# leader finish (idempotent)
with lock:
    if key not in inflight_map and slot[0] is not None:
        return payload
    slot[0] = copy.deepcopy(payload)
    inflight_map.pop(key, None)
    event.set()
```

2) Select and write shared destinations (processes)
- Never decide “this path is free” using `.exists()` under concurrency.
- Atomically reserve the destination up front (e.g., `O_CREAT|O_EXCL`) and treat that reservation as the source of truth.
- Pass the exact claimed path/handle into all downstream logic (including user-visible text like footers) so concurrent runs can’t diverge.

Checklist
- Is there exactly one owner (leader/reserver) per shared key/resource?
- Do all non-owners wait/block on that owner’s completion signal, rather than timing guesses?
- For shared outputs, did you atomically reserve and then reuse the same claimed path/handle everywhere (not just for the actual write)?
- Is the “publish/finish” logic safe against double execution (idempotent)?
