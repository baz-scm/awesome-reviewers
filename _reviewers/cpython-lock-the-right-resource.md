---
title: Lock the right resource
description: 'When protecting shared mutable state, make sure the synchronization
  actually covers the memory that other threads can see and mutate, and scope it correctly:'
repository: python/cpython
label: Concurrency
language: C
comments_count: 10
repository_stars: 77696
---

When protecting shared mutable state, make sure the synchronization actually covers the memory that other threads can see and mutate, and scope it correctly:

1. Lock the real object in place, never a copy. Taking a mutex by value and locking the copy (`PyMutex mutex = interp->runtime->audit_hooks.mutex; PyMutex_Lock(&mutex);`) silently locks a stack-local object and does nothing to the shared one. Always take the address of the shared field: `PyMutex_Lock(&interp->runtime->audit_hooks.mutex);`.

2. Hold the lock that actually owns the data you are touching. If a field is protected by a different object's critical section (e.g. a context's buffer read while only the socket's lock is held), another thread can free/replace it concurrently. Acquire the critical section of the object that owns the field, not an unrelated one.

3. Scope critical sections to the operation, not to every iteration or every low-level helper. Don't re-acquire a lock inside a loop body when the whole loop can be covered by one critical section (factor the body into a `*_lock_held` helper); and don't add locking inside allocation/init/dealloc/traverse/clear helpers — by the time these run, the object is either not yet shared or is already being torn down under GC guarantees, so locking there is both unnecessary and can be unsafe for callers that already hold the lock.

4. For simple fields read and written from multiple threads without a critical section (reference-like counters, cached flags, cell contents), use the project's atomic accessors (`FT_ATOMIC_ADD_SSIZE`, `FT_ATOMIC_LOAD/STORE_*`, `PyCell_GetRef`) consistently, matching how the rest of the codebase accesses that field — a plain `exports++` or a raw pointer dereference next to atomic updates elsewhere is a data race.

Example:
```c
/* Wrong: copies the mutex; locks a stack-local object */
PyMutex mutex = interp->runtime->audit_hooks.mutex;
PyMutex_Lock(&mutex);

/* Right: lock the shared mutex directly */
PyMutex_Lock(&interp->runtime->audit_hooks.mutex);

/* Wrong: plain increment races with concurrent atomic updates elsewhere */
((PyMemoryViewObject *)v)->exports++;

/* Right: use the same atomic macro used by other call sites */
FT_ATOMIC_ADD_SSIZE(((PyMemoryViewObject *)v)->exports, 1);
```

Before adding or reviewing a `Py_BEGIN_CRITICAL_SECTION`/atomic access, ask: is this the object that truly owns the data, is this the minimal scope needed, and does it match the access pattern used everywhere else for that field?