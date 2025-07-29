---
title: async cleanup safety
description: Ensure async operations include proper safety checks to prevent race
  conditions, memory leaks, and inconsistent state. This includes equality checks
  before updates, destruction status verification, and proper cleanup mechanisms.
repository: sveltejs/svelte
label: Concurrency
language: JavaScript
comments_count: 3
repository_stars: 83580
---

Ensure async operations include proper safety checks to prevent race conditions, memory leaks, and inconsistent state. This includes equality checks before updates, destruction status verification, and proper cleanup mechanisms.

Key safety patterns to implement:
- **Equality checks**: Always verify `!source.equals(value)` before applying updates in async contexts to prevent unnecessary side effects
- **Destruction checks**: Verify effects haven't been destroyed before adding dependencies: `var destroyed = active_effect !== null && (active_effect.f & DESTROYED) !== 0`
- **Memory leak prevention**: Use WeakRef or similar patterns for long-lived async objects that reference reactions

Example of unsafe vs safe async operation:
```js
// Unsafe - missing equality check
export function simple_set(source, value) {
  source.v = value;
  source.o?.onchange?.(); // fires even when value unchanged
}

// Safe - includes equality check
export function set(source, value) {
  if (!source.equals(value)) {
    source.v = value;
    source.o?.onchange?.();
  }
}
```

The "simple" optimization often becomes a "bug magnet" by removing essential safety checks that prevent race conditions in concurrent scenarios.