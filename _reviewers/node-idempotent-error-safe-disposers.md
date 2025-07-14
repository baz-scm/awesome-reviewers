---
title: Idempotent error-safe disposers
description: 'When implementing resource cleanup logic, especially disposers for explicit
  resource management, always design for resilience during error conditions:'
repository: nodejs/node
label: Error Handling
language: Markdown
comments_count: 11
repository_stars: 112178
---

When implementing resource cleanup logic, especially disposers for explicit resource management, always design for resilience during error conditions:

1. Make disposal methods idempotent - they should work correctly when called multiple times without side effects
2. Avoid throwing errors from disposers - thrown exceptions in cleanup code can mask original errors in a `SuppressedError`
3. Always assume disposers may be called during exception handling - they receive no information about whether an exception is pending

```js
class MyDisposableResource {
  #disposed = false;
  
  dispose() {
    // ✅ Idempotent - safe to call multiple times
    if (this.#disposed) return;
    this.#disposed = true;
    
    try {
      // Cleanup logic here
      console.log('Resource cleaned up');
    } catch (error) {
      // ✅ Avoid throwing from disposers
      console.error('Error during disposal:', error);
      // Don't re-throw - this would mask any pending exception
    }
  }

  [Symbol.dispose]() {
    // ✅ Delegate to explicit disposal method
    this.dispose();
  }
}
```

This pattern ensures resources are cleaned up reliably even during error conditions. By making disposers idempotent and error-safe, you prevent cascading failures where cleanup code compounds the original problem. It's especially important in `using`/`await using` blocks where disposers are called automatically during both normal and exceptional exits, with no information about pending exceptions.