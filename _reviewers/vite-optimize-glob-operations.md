---
title: Optimize glob operations
description: 'When using glob patterns for file system operations, ensure optimal
  performance and consistent behavior by configuring glob libraries appropriately
  and handling paths efficiently:'
repository: vitejs/vite
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 74031
---

When using glob patterns for file system operations, ensure optimal performance and consistent behavior by configuring glob libraries appropriately and handling paths efficiently:

1. **Specify correct options** for your glob library:
   - Set `expandDirectories: false` when replacing libraries like fast-glob with alternatives that have different defaults
   - Use `absolute: true` when you need absolute paths in results
   - Set appropriate `cwd` to limit search scope and improve performance

```javascript
// Less efficient: may search unnecessary directories
const files = globSync(pattern, {
  ignore: ['**/node_modules/**']
})

// More efficient: properly scoped search with correct options
const files = globSync(pattern, {
  cwd: path.resolve(path.dirname(id), dir),
  absolute: true, 
  expandDirectories: false,
  ignore: ['**/node_modules/**']
})
```

2. **Handle path normalization** consistently by:
   - Normalizing paths before using them in glob patterns
   - Using regex for efficient path extraction when dealing with complex patterns
   - Setting appropriate options for dotfile handling (`dot: true`) when needed

3. **Optimize node_modules handling** in glob patterns:
   - Use regex-based extraction for path segments to avoid unnecessary file traversal
   - Implement path rebasing for patterns that include node_modules to ensure ignore patterns work correctly

Remember that glob operations are computationally expensive, so always consider the algorithmic efficiency of your approach when working with large directory trees.