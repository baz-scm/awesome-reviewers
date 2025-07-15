---
title: Pause tracking during side-effects
description: When executing side-effects in reactive systems (like event handlers,
  cleanup functions, or async operations), always pause reactivity tracking to prevent
  unintended dependencies from being captured. This prevents infinite loops, race
  conditions, and unexpected behavior that can occur when reactive state is accessed
  during side-effects.
repository: vuejs/core
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 50769
---

When executing side-effects in reactive systems (like event handlers, cleanup functions, or async operations), always pause reactivity tracking to prevent unintended dependencies from being captured. This prevents infinite loops, race conditions, and unexpected behavior that can occur when reactive state is accessed during side-effects.

Use `pauseTracking()` before and `resetTracking()` after such operations, and ensure tracking is reset even when errors occur by using try/finally blocks:

```js
// Bad: Side-effect might track unwanted dependencies
function handleEvent() {
  callEventHandler();  // Might access reactive state
}

// Good: Pausing tracking during side-effect
function handleEvent() {
  pauseTracking();
  try {
    callEventHandler();  // Safe to access reactive state
  } finally {
    resetTracking();  // Always reset, even if errors occur
  }
}
```

For reusable patterns, consider implementing pausable effects:

```js
class PausableEffect extends ReactiveEffect {
  private _isPaused = false;
  
  pause() {
    this._isPaused = true;
  }
  
  resume() {
    this._isPaused = false;
    // Additional logic as needed
  }
  
  update() {
    if (!this._isPaused) {
      return super.run();
    }
  }
}
```

This pattern is essential for maintaining reactivity system integrity, especially when dealing with event handlers, cleanup functions, and asynchronous operations that could otherwise cause unpredictable behavior or performance issues.