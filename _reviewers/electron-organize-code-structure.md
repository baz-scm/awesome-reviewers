---
title: organize code structure
description: Make deliberate structural decisions that improve code maintainability
  and readability. Consider the appropriate implementation layer, proper encapsulation
  patterns, and logical organization of code components.
repository: electron/electron
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 117644
---

Make deliberate structural decisions that improve code maintainability and readability. Consider the appropriate implementation layer, proper encapsulation patterns, and logical organization of code components.

Key principles:
- Use truly private functions instead of underscore-prefixed "private" methods to avoid abuse: `function awaitNextLoad(...` instead of `WebContents.prototype._awaitNextLoad`
- Choose the optimal implementation layer for maintainability - move logic to C++ when it reduces code spread across files and improves efficiency
- Organize tests logically with descriptive names rather than excessive nesting: `it('returns image with requested size when both dimensions are bigger', async () => {` instead of multiple nested `describe` blocks
- Prioritize fewer files with clearer responsibilities over scattered implementations

Example of proper encapsulation:
```typescript
// Instead of:
WebContents.prototype._awaitNextLoad = function (navigationUrl: string) {
  // implementation
}

// Use:
function awaitNextLoad(navigationUrl: string) {
  // implementation
}
// Then call with: return awaitNextLoad.call(this)
```

This approach reduces code complexity, improves maintainability, and makes the codebase easier to navigate and understand.