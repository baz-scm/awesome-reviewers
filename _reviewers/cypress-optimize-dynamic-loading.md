---
title: optimize dynamic loading
description: When using dynamic imports, implement timing controls and strategic naming
  to ensure reliable and efficient resource loading. Use minimal delays (like setTimeout
  with 0ms) to control initialization timing and prevent race conditions that could
  cause failures. Additionally, use descriptive chunk names with webpackChunkName
  comments to create readable,...
repository: cypress-io/cypress
label: Performance Optimization
language: JavaScript
comments_count: 2
repository_stars: 48850
---

When using dynamic imports, implement timing controls and strategic naming to ensure reliable and efficient resource loading. Use minimal delays (like setTimeout with 0ms) to control initialization timing and prevent race conditions that could cause failures. Additionally, use descriptive chunk names with webpackChunkName comments to create readable, manageable bundles that improve system organization and API handling.

Example:
```javascript
// Use timing control to ensure proper initialization
const importsToLoad = [() => {
  return new Promise((resolve) => {
    setTimeout(() => {
      import(/* @vite-ignore */ specPath).then(resolve)
    }, 0) // Use 0ms for next tick timing
  })
}]

// Use descriptive chunk names for better organization
const eventManager = await import(/* webpackChunkName: "ctChunk-EventManager" */'./event-manager')
  .then((module) => module.default)
```

This approach prevents resource loading failures while maintaining organized, performant code splitting that benefits both development and runtime performance.