---
title: Isolate DOM security boundaries
description: When developing UI components, establish clear DOM manipulation boundaries
  to prevent security risks. Components that modify aria attributes (like aria-hidden)
  on parent or ancestor elements can create security vulnerabilities by unexpectedly
  exposing content that was intentionally hidden from assistive technologies or hiding
  content that should be...
repository: mui/material-ui
label: Security
language: TypeScript
comments_count: 2
repository_stars: 96063
---

When developing UI components, establish clear DOM manipulation boundaries to prevent security risks. Components that modify aria attributes (like aria-hidden) on parent or ancestor elements can create security vulnerabilities by unexpectedly exposing content that was intentionally hidden from assistive technologies or hiding content that should be accessible.

For example, in the code below, removing aria-hidden attributes from ancestor elements might expose content that was intentionally hidden for security reasons:

```javascript
// Risky pattern - modifies DOM outside component boundaries
function ariaHiddenElements(container, mountElement, currentElement, elementsToExclude, show) {
  let current = container;
  
  while (current != null && html !== current) {
    // Traversing up the DOM tree
    for (let i = 0; i < current.children.length; i += 1) {
      // Removing aria-hidden could expose sensitive content
      if (isPreviousElement && !isNotExcludedElement && show) {
        ariaHidden(element, !show); // Removes aria-hidden
      }
    }
    current = current.parentElement;
  }
}
```

Instead, limit aria attribute modifications to elements within your component's scope, or provide clear documentation and configuration options if cross-boundary modifications are necessary for functionality. If you must modify parent elements, implement a tracking mechanism to distinguish between attributes set by your component versus those set intentionally by developers for security purposes.