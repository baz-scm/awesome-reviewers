---
title: async resource cleanup
description: Always ensure proper cleanup of asynchronous resources (subscriptions,
  timeouts, event listeners) to prevent memory leaks and race conditions. Use Angular's
  DestroyRef or similar lifecycle management patterns instead of manual cleanup.
repository: angular/angular
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 98611
---

Always ensure proper cleanup of asynchronous resources (subscriptions, timeouts, event listeners) to prevent memory leaks and race conditions. Use Angular's DestroyRef or similar lifecycle management patterns instead of manual cleanup.

When working with subscriptions, timeouts, or event listeners, establish cleanup mechanisms at the point of creation. This prevents resources from outliving their intended lifecycle and causing unexpected behavior in concurrent scenarios.

Example of proper cleanup pattern:
```typescript
// Good: Using DestroyRef for automatic cleanup
constructor(private destroyRef: DestroyRef) {
  const subscription = router.events.subscribe((s: Event) => {
    if (s instanceof NavigationEnd) {
      this.update();
    }
  });
  this.destroyRef.onDestroy(() => subscription.unsubscribe());
}

// Good: Timeout with cleanup consideration
const timeout = setTimeout(() => removeFn(), ANIMATION_TIMEOUT);
details.animateFn(() => {
  clearTimeout(timeout);
  removeFn();
});
```

For event listeners on elements that will be removed from the DOM, cleanup may be automatic, but for long-lived subscriptions and timers, explicit cleanup is essential to maintain application stability and prevent resource exhaustion.