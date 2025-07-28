---
title: Early returns prevent waste
description: Add early return statements and duplicate checks to avoid unnecessary
  computations, memory allocations, and API calls. This pattern prevents performance
  degradation by stopping expensive operations before they begin.
repository: facebook/react-native
label: Performance Optimization
language: JavaScript
comments_count: 5
repository_stars: 123178
---

Add early return statements and duplicate checks to avoid unnecessary computations, memory allocations, and API calls. This pattern prevents performance degradation by stopping expensive operations before they begin.

Key strategies:
1. **Check for duplicates before adding to collections** to prevent memory leaks
2. **Validate preconditions early** to avoid unnecessary processing
3. **Return immediately when work is not needed** instead of continuing execution

Example implementation:
```javascript
__addChild(child: AnimatedNode): void {
  // Prevent adding duplicate animated nodes
  if (this._children.includes(child)) {
    return;
  }
  // Continue with expensive operations only if needed
  this._children.push(child);
  // ... rest of implementation
}

_maybeCallOnEndReached() {
  const {onEndReached} = this.props;
  // Early return if callback doesn't exist
  if (!onEndReached) {
    return;
  }
  // Early return if scrolling in wrong direction
  if (offset <= 0 || dOffset <= 0) {
    return;
  }
  // ... continue with expensive calculations
}
```

This approach reduces unnecessary memory allocations, prevents duplicate processing, and eliminates redundant API calls, leading to better overall performance and resource utilization.