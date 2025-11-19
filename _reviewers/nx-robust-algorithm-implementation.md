---
title: robust algorithm implementation
description: Implement algorithms that handle edge cases and avoid brittle assumptions
  about input data or structure formats. Instead of relying on simple string manipulation
  or assuming data structure behavior, use comprehensive approaches that account for
  various scenarios.
repository: nrwl/nx
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 27518
---

Implement algorithms that handle edge cases and avoid brittle assumptions about input data or structure formats. Instead of relying on simple string manipulation or assuming data structure behavior, use comprehensive approaches that account for various scenarios.

For parsing operations, handle multiple input formats:
```javascript
// Brittle approach
const target = task.target.target.split('--')[0];
const lines = content.split('\n');

// Robust approach  
const target = getTargetFromMetadata(task, projectGraph);
const lines = content.split(/\r\n|\r|\n/);
```

For data structure access, verify assumptions and implement proper traversal:
```javascript
// Assumption-based approach
const children = reflection.children;

// Verified approach
const childReflections = reflections.filter(
  (r) => r.parent && r.parent.id === reflection.id
);
```

This approach prevents bugs caused by incomplete parsing, platform differences, or incorrect assumptions about data structure behavior, leading to more reliable and maintainable code.