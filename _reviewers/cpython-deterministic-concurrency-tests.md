---
title: Deterministic concurrency tests
description: 'When writing tests that try to trigger a race condition or verify thread-safety,
  do not rely on implicit timing (e.g. just calling `Thread.start()` and hoping the
  scheduler interleaves correctly, or sprinkling `time.sleep()` calls) to hit the
  narrow window under test. Such tests are flaky: they may pass hundreds of times
  and still miss the bug, or...'
repository: python/cpython
label: Concurrency
language: Python
comments_count: 5
repository_stars: 77696
---

When writing tests that try to trigger a race condition or verify thread-safety, do not rely on implicit timing (e.g. just calling `Thread.start()` and hoping the scheduler interleaves correctly, or sprinkling `time.sleep()` calls) to hit the narrow window under test. Such tests are flaky: they may pass hundreds of times and still miss the bug, or intermittently fail for unrelated reasons. Instead, use explicit synchronization primitives to force all threads to start together and to force execution to pause exactly where the race needs to happen:

- Use a `threading.Barrier` (or the `threading_helper.run_concurrently` helper) to start all test threads at the same instant instead of looping over `Thread.start()`.
- When a specific interleaving is required (e.g. "thread B must observe the lock held by thread A"), poll or wait on the actual lock/queue involved rather than assuming a `start()` call already produced the desired state. For example, spin on `lock.acquire(block=False)` until it fails, or use `Event.wait()` with a small timeout, to deterministically confirm the other thread reached the critical section.
- Prefer existing test helpers (`threading_helper.run_concurrently`, `threading_helper.join_thread`, `threading_helper.start_threads`) over hand-rolled thread management; they already handle correct startup synchronization and safe cleanup (e.g. avoiding double-closing shared resources when a timeout fires).

Example of forcing a deterministic handoff instead of a hopeful `start()`:

```python
filler = threading.Thread(target=queue.put, args=(data,))
filler.start()
wlock = queue._wlock
# Wait until the filler is actually holding the write lock
# instead of assuming start() already got there.
while wlock.acquire(block=False):
    wlock.release()
    time.sleep(0.001)
```

Applying this consistently turns intermittent, hard-to-reproduce race tests into reliable regression tests that will reliably fail without the underlying fix and reliably pass with it.