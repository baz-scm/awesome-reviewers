---
title: Handle component edge cases
description: When implementing functionality for React components, especially for
  specialized component types like Fragments and Portals, always include defensive
  checks for edge cases such as unmounted components or conditional traversal requirements.
repository: facebook/react
label: React
language: Javascript
comments_count: 2
repository_stars: 236926
---

When implementing functionality for React components, especially for specialized component types like Fragments and Portals, always include defensive checks for edge cases such as unmounted components or conditional traversal requirements.

Consider the component's lifecycle state and implement appropriate fallbacks:

```javascript
// Example: Handling unmounted components
SomeComponent.prototype.someMethod = function(this: ComponentType, arg: any): returnType {
  const parentInstance = getParentInstance(this._fiber);
  
  // Defensive check for unmounted component
  if (parentInstance === null) {
    return FALLBACK_VALUE; // Return appropriate fallback
  }
  
  // Normal operation when mounted
  return parentInstance.someOperation(arg);
};

// Example: Conditional traversal based on component type
function traverseChildren(fiber, callback, skipSpecialTypes = false) {
  let child = fiber.child;
  
  while (child !== null) {
    // Skip special component types conditionally
    if (skipSpecialTypes && (child.tag === Portal || child.tag === SpecialType)) {
      // Skip this type based on operation context
    } else {
      callback(child);
      traverseChildren(child, callback, skipSpecialTypes);
    }
    child = child.sibling;
  }
}
```

This approach prevents runtime errors, improves component stability, and ensures consistent behavior across different component states and edge cases in the React component lifecycle.