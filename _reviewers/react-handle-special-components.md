---
title: Handle special components
description: When implementing functionality that interacts with React's component
  model, ensure special component types (fragments, portals, etc.) are handled appropriately
  for their specific contexts. Different component types may require conditional logic
  based on their current state or the operation being performed.
repository: facebook/react
label: React
language: Javascript
comments_count: 2
repository_stars: 236926
---

When implementing functionality that interacts with React's component model, ensure special component types (fragments, portals, etc.) are handled appropriately for their specific contexts. Different component types may require conditional logic based on their current state or the operation being performed.

For example:

1. When working with Fragment instances, always check if they're mounted before performing DOM operations:
```javascript
FragmentInstance.prototype.someMethod = function(this: FragmentInstanceType) {
  const parentHostInstance = getFragmentParentHostInstance(this._fragmentFiber);
  if (parentHostInstance === null) {
    // Handle unmounted case appropriately
    return FALLBACK_VALUE;
  }
  // Continue with normal operation
};
```

2. For component traversal, consider whether special components like portals should be included based on the operation:
```javascript
function traverseComponents(child, operation) {
  if (child.tag === HostPortal && operation.type === 'layout') {
    // Skip portals for layout operations
  } else {
    // Process component
    processChild(child, operation);
  }
}
```

This approach prevents bugs related to component lifecycle states and ensures consistent behavior across different React component types.