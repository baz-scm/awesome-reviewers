---
title: Avoid repeated object creation
description: Prevent performance degradation by avoiding the creation of functions,
  objects, regular expressions, and other expensive operations inside loops or frequently
  executed code paths. Instead, hoist these creations outside the loop or to a higher
  scope where they can be reused.
repository: TanStack/router
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 11590
---

Prevent performance degradation by avoiding the creation of functions, objects, regular expressions, and other expensive operations inside loops or frequently executed code paths. Instead, hoist these creations outside the loop or to a higher scope where they can be reused.

This optimization is particularly important in performance-critical sections like routing logic, data processing loops, and render functions where the same operation may be executed hundreds or thousands of times.

Examples of what to avoid:
```javascript
// Bad: Function created on every iteration
for (const [index, match] of matches.entries()) {
  function makeMaybe(value, error) {
    if (error) return { status: 'error', error }
    return { status: 'success', value }
  }
  // use makeMaybe...
}

// Bad: Regex created on every filter call
items.filter(d => !d.name.match(new RegExp(pattern, 'g')))
```

Better approach:
```javascript
// Good: Function hoisted outside the loop
function makeMaybe(value, error) {
  if (error) return { status: 'error', error }
  return { status: 'success', value }
}

for (const [index, match] of matches.entries()) {
  // use makeMaybe...
}

// Good: Regex created once
const regex = new RegExp(pattern, 'g')
items.filter(d => !d.name.match(regex))
```

This practice reduces memory allocation overhead, garbage collection pressure, and improves execution speed in performance-sensitive code paths.