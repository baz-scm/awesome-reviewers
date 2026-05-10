---
title: Thread Ownership Discipline
description: 'When code can run on both main and IO threads, require an explicit ownership
  + synchronization rule for every shared piece of state (flags, counters, refcounts,
  pending lists, and memory frees). Concretely:'
repository: redis/redis
label: Concurrency
language: C
comments_count: 9
repository_stars: 74261
---

When code can run on both main and IO threads, require an explicit ownership + synchronization rule for every shared piece of state (flags, counters, refcounts, pending lists, and memory frees). Concretely:

1) No racy reads/writes of shared fields
- Avoid reading/writing client flags/state from the “wrong” thread unless protected (atomics) or guaranteed single-writer.
- If IO thread must notify main, set a thread-safe “pending” flag/queue and return.

2) Main-thread only for shared sliding-window / non-thread-safe maintenance
- Shared maintenance structures (e.g., active-clients windows) should be updated in one place (main thread) to avoid races; use atomics only for standalone counters.

3) Refcount changes must be atomic end-to-end
- Don’t do atomicGet then a non-atomic decrement. Use atomic decrement operations that provide the resulting value, so concurrent decrRefCount cannot double-free.

4) If deallocation/free callbacks are not thread-safe: defer to the safe thread
- If decrRefCount/free may run in background threads, ensure free callbacks are thread-safe or document that they may run off the main thread.
- Prefer an IO->main deferred-free queue for objects that must be freed on main.
- Keep queue state consistent (reset counters/size as needed) and consider splitting responsibilities (freeing vs unlinking from “pending reply” lists).

Example patterns

A) IO thread signals main using a pending flag instead of touching racy state
```c
if (!(c->io_flags & CLIENT_IO_READ_ENABLED)) {
    /* No racy reads of c->flags; just signal via atomic pending flag */
    atomicSetWithSync(c->pending_read, 1);
    return;
}
```

B) Main-thread-only maintenance
```c
atomicIncr(server.stat_total_client_process_input_buff_events, 1);
if (c->running_tid == IOTHREAD_MAIN_THREAD_ID)
    statsUpdateActiveClients(c);
```

C) Safe atomic refcount decrement
```c
unsigned short new_refcnt = atomicDecr(o->refcount, 1);
if (new_refcnt == 0) {
    /* safe to free */
}
```

D) Deferred free from IO thread to main
```c
/* IO thread */
ioDeferFreeRobj(c, obj);

/* main thread when client is back */
freeClientIODeferredObjects(c, /*free_array=*/0);
```

Documentation requirement
- Any module/type free callback that can run off-main must explicitly state its thread-safety assumptions (e.g., “may run in a background thread; not protected by GIL/GCIL”).