---
title: Cancellation-Aware Async
description: 'Ensure any async work that mutates shared state or UI is *cancellation-
  and identity-safe*: after every `await` (especially inside queued/limited execution),
  re-validate that the operation is still the current one, and pass the cancellation
  token into the work.'
repository: microsoft/VSCode
label: Concurrency
language: TypeScript
comments_count: 7
repository_stars: 194303
---

Ensure any async work that mutates shared state or UI is *cancellation- and identity-safe*: after every `await` (especially inside queued/limited execution), re-validate that the operation is still the current one, and pass the cancellation token into the work.

Apply this whenever:
- you enqueue work behind a limiter/queue;
- you start async fetches on user input/navigation;
- you render from async sources (e.g., README/metadata) that may overlap;
- you restore multiple items on startup.

**Guideline**
1) Use an operation “generation” (or request identity) captured at start.
2) After `await`, check `generation === currentGeneration` and `!token.isCancellationRequested` (and also `!store.isDisposed` / `element.isConnected` where relevant).
3) If work is queued, recheck cancellation and identity inside the limiter factory, not only at enqueue time.
4) For overlapping renders, use a render-generation guard so only the latest completion can update the DOM.

**Example pattern (limiter + generation + token pass-through)**
```ts
class Example extends Disposable {
  private generation = 0;
  private readonly limiter = createLimiter({ concurrency: 2 });

  refresh(token: CancellationToken) {
    const myGen = ++this.generation;
    void this.limiter.queue(async () => {
      // Recheck at execution time (queued work can become stale)
      if (token.isCancellationRequested || this.isDisposed || myGen !== this.generation) {
        return;
      }

      // Do the awaited work with the token
      const result = await computeExpensiveThing({ token });

      // Recheck again before mutating UI/state
      if (token.isCancellationRequested || myGen !== this.generation || this.isDisposed) {
        return;
      }
      this.updateUI(result);
    });
  }
}
```

This prevents:
- stale async completions overwriting newer results;
- fan-out spikes from restores/load;
- cancellation not being honored once work starts;
- overlapping async renders duplicating content or updating detached/disposed UI.