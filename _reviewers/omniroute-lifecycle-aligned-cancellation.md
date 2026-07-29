---
title: Lifecycle-aligned Cancellation
description: When handling concurrent async work (streaming, tees, semaphores/limits,
  watchdogs), ensure cancellation, timeouts, and accounting are tied to the *actual*
  consumer lifecycle—release/decrement/teardown at the point where the work is truly
  finished, and don’t block on cancellation promises that can’t resolve until another
  branch drains.
repository: diegosouzapw/OmniRoute
label: Concurrency
language: TypeScript
comments_count: 6
repository_stars: 33162
---

When handling concurrent async work (streaming, tees, semaphores/limits, watchdogs), ensure cancellation, timeouts, and accounting are tied to the *actual* consumer lifecycle—release/decrement/teardown at the point where the work is truly finished, and don’t block on cancellation promises that can’t resolve until another branch drains.

Practical rules:
- **Don’t await cancellation of detached/tee branches** if it may remain pending until another consumer drains; cancel and proceed.
- **Release concurrency slots only after the stream is fully consumed** (e.g., `TransformStream.flush`/end-of-stream), not when headers/initial chunks arrive.
- **Prevent double accounting**: if you decrement pending counters at multiple phases (e.g., flush + handler), gate with a flag or ensure only one phase decrements.
- **Use abort timeouts for network calls** and merge with any provided AbortSignal so requests can’t hang indefinitely.
- **Guard watchdog math**: if the baseline timestamp/listener wiring can be missing, seed it or skip instead of computing stall against `undefined`.

Example pattern (release on flush, not header arrival):
```ts
const slot = await acquireSemaphore();
let released = false;
const releaseOnce = () => {
  if (released) return;
  released = true;
  slot();
};

return new TransformStream<Uint8Array, Uint8Array>({
  transform(chunk, controller) {
    controller.enqueue(chunk);
  },
  flush() {
    // stream fully consumed (client drained)
    releaseOnce();
  }
});
```

These practices reduce race conditions, deadlocks, leaked capacity, and spurious failures in highly concurrent streaming systems.