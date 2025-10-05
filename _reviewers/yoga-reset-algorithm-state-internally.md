---
title: Reset algorithm state internally
description: Algorithms should handle their own state initialization and cleanup internally
  rather than relying on callers to manage it. This prevents bugs caused by stale
  data from previous executions and reduces the burden on calling code.
repository: facebook/yoga
label: Algorithms
language: JavaScript
comments_count: 2
repository_stars: 18255
---

Algorithms should handle their own state initialization and cleanup internally rather than relying on callers to manage it. This prevents bugs caused by stale data from previous executions and reduces the burden on calling code.

When designing algorithms that maintain state between calls or process hierarchical data structures, ensure that:

1. **Internal reset logic**: The algorithm resets relevant state at the beginning of execution
2. **Encapsulated cleanup**: State management is contained within the algorithm implementation
3. **Caller independence**: External code doesn't need to perform setup/teardown operations

Example from layout algorithm:
```javascript
function layoutNode(node, parentMaxWidth, parentDirection) {
  // Algorithm handles its own state reset internally
  if (!node.lastLayout) {
    node.lastLayout = {};
  }
  
  // Reset child layouts internally rather than requiring caller to do it
  // This prevents stale position data from affecting current calculations
  resetChildLayouts(node);
  
  // Continue with algorithm logic...
}
```

This approach prevents issues where "isUndefined checks might fail where they shouldn't" and ensures "the callsite doesn't have to care and possibly introduce bugs" by forgetting to reset state properly.