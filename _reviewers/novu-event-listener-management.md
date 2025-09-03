---
title: Event listener management
description: Implement comprehensive event listener management by registering listeners
  on multiple relevant sources and providing appropriate fallback mechanisms. This
  ensures robust event handling across different environments and prevents missed
  events that could lead to inconsistent application state.
repository: novuhq/novu
label: Networking
language: TSX
comments_count: 2
repository_stars: 37700
---

Implement comprehensive event listener management by registering listeners on multiple relevant sources and providing appropriate fallback mechanisms. This ensures robust event handling across different environments and prevents missed events that could lead to inconsistent application state.

When handling events that may originate from multiple sources, register listeners on all relevant targets rather than relying on a single source. Additionally, implement feature detection and fallbacks for environments that may not support newer APIs.

Example implementation:
```typescript
// Register on multiple event sources
document.body.addEventListener('click', handleClickOutside);
containerElement()?.addEventListener('click', handleClickOutside);

// Use feature detection with fallbacks
const supportsInterpolateSize = CSS.supports('interpolate-size', 'allow-keywords');
if (contentRef && !supportsInterpolateSize) {
  resizeObserver.observe(contentRef);
}

// Ensure proper cleanup
onCleanup(() => {
  document.body.removeEventListener('click', handleClickOutside);
  containerElement()?.removeEventListener('click', handleClickOutside);
  resizeObserver.disconnect();
});
```

This pattern is particularly important for network event handling where events may come from multiple connection sources, protocols, or fallback mechanisms, and proper cleanup prevents resource leaks in long-running network applications.