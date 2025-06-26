---
title: "Optimize hot paths"
description: "In performance-critical code paths that execute frequently, optimize to reduce unnecessary operations that can impact runtime performance."
repository: "facebook/react"
label: "Performance Optimization"
language: "JavaScript"
comments_count: 4
repository_stars: 237000
---

In performance-critical code paths that execute frequently, optimize to reduce unnecessary operations that can impact runtime performance:

1. **Minimize repeated type checks** - Cache type information or restructure code to avoid redundant `typeof` calls, especially in loops or frequently called functions

2. **Avoid unnecessary allocations** - Don't create new arrays, Sets, or objects when you can work with existing data structures directly

3. **Use direct traversal** - When operating on DOM nodes or other hierarchical structures, prefer inline traversal over building intermediate collections:

```javascript
// Avoid this in hot paths
const children = new Set(); // Unnecessary allocation
elements.forEach(el => children.add(el));
children.forEach(child => child.addEventListener(type, listener));

// Prefer this approach
elements.forEach(el => el.addEventListener(type, listener));
```

4. **Be aware of thresholds** - Understand the impact of operations based on execution frequency:
    - <1ms: Optimal for very frequent operations
    - <10ms: Good for maintaining 60fps animations
    - <100ms: Maximum for responsive interactions

Operations that take more time should be candidates for optimization when they appear in hot paths.