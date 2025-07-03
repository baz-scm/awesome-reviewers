---
title: Handle special component types
description: When working with React's special component types like Fragments and
  Portals, always handle their unique behaviors and lifecycle states appropriately.
  These components require special consideration for operations like DOM traversal,
  position comparison, and event handling.
repository: facebook/react
label: React
language: Javascript
comments_count: 2
repository_stars: 236925
---

When working with React's special component types like Fragments and Portals, always handle their unique behaviors and lifecycle states appropriately. These components require special consideration for operations like DOM traversal, position comparison, and event handling.

For Fragments:
- Always check if a Fragment is mounted before performing DOM operations
- Remember that Fragments don't have a direct DOM node representation

For Portals:
- Consider whether portal children should be included in traversals based on the operation context (layout vs events)

Example:
```javascript
// When implementing DOM-related methods for Fragments
FragmentInstance.prototype.someMethod = function(params) {
  const parentHostInstance = getFragmentParentHostInstance(this._fragmentFiber);
  
  // Always check for unmounted fragments
  if (parentHostInstance === null) {
    // Handle disconnected/unmounted case appropriately
    return DISCONNECTED_VALUE;
  }
  
  // Continue with normal operation
  return parentHostInstance.someMethod(params);
};

// When traversing components, consider whether to skip certain types
function traverseComponents(component, skipPortals) {
  // ...
  
  if (skipPortals && child.tag === HostPortal) {
    // Skip portals when appropriate for the context
    continue;
  }
  
  // Continue traversal...
}
```

This approach prevents subtle bugs related to React's component architecture and ensures consistent behavior across different rendering scenarios.