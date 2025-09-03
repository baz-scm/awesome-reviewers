---
title: function decomposition clarity
description: Functions should be focused, concise, and easy to understand. Break down
  large functions (>100 lines) into smaller, well-named functions that each handle
  a single responsibility. Remove unused parameters to reduce cognitive load and prevent
  confusion. Prefer functional programming patterns like `.some()`, `.map()`, and
  `.filter()` over imperative loops when...
repository: cypress-io/cypress
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 48850
---

Functions should be focused, concise, and easy to understand. Break down large functions (>100 lines) into smaller, well-named functions that each handle a single responsibility. Remove unused parameters to reduce cognitive load and prevent confusion. Prefer functional programming patterns like `.some()`, `.map()`, and `.filter()` over imperative loops when they improve readability. Use proper async/await patterns instead of mixing promise styles.

Example of improvement:
```typescript
// Before: Large function with unused parameter
async function processData(data: any[], _unusedFlag?: boolean) {
  // 150+ lines of mixed logic
  let results = []
  data.forEach((item) => {
    if (item.isValid && item.hasPermission && item.isActive) {
      results.push(item)
    }
  })
  // more complex logic...
}

// After: Decomposed with functional patterns
async function processData(data: any[]) {
  const validItems = filterValidItems(data)
  const processedItems = await processItems(validItems)
  return formatResults(processedItems)
}

function filterValidItems(data: any[]) {
  return data.filter(item => 
    item.isValid && item.hasPermission && item.isActive
  )
}
```

This approach makes code more testable, readable, and maintainable by reducing complexity and making each function's purpose clear.