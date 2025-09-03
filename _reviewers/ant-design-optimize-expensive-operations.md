---
title: Optimize expensive operations
description: Minimize performance impact of costly operations through strategic ordering,
  batching, and avoiding unnecessary work. Place cheaper conditional checks before
  expensive operations to enable early exits, batch DOM manipulations using requestAnimationFrame
  to reduce repaints, and ensure optimizations don't create additional computational
  overhead.
repository: ant-design/ant-design
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 95882
---

Minimize performance impact of costly operations through strategic ordering, batching, and avoiding unnecessary work. Place cheaper conditional checks before expensive operations to enable early exits, batch DOM manipulations using requestAnimationFrame to reduce repaints, and ensure optimizations don't create additional computational overhead.

For conditional checks, evaluate lightweight operations first:
```typescript
// Good: Check cheap operations first
if (ele.scrollWidth > ele.clientWidth || ele.scrollHeight > ele.clientHeight) {
  return true;
}
// Only execute expensive DOM operations if needed
const rect = ele.getBoundingClientRect();
const childRect = childDiv.getBoundingClientRect();
```

For DOM operations, use requestAnimationFrame to batch updates:
```typescript
let isScheduled = false;

const adjustElementWidth = (width: number, wrapper: HTMLElement): void => {
  if (!isScheduled) {
    isScheduled = true;
    requestAnimationFrame(() => {
      wrapper.style.width = `${width + ELEMENT_GAP}px`;
      isScheduled = false;
    });
  }
};
```

Verify that optimizations actually reduce work rather than creating additional iterations or computations. Profile performance-critical code paths to ensure improvements deliver measurable benefits.