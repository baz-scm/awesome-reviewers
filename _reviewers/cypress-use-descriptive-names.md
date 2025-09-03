---
title: Use descriptive names
description: 'Choose names that clearly reveal the purpose and behavior of variables,
  functions, and methods. Names should be self-documenting and follow these patterns:'
repository: cypress-io/cypress
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 48850
---

Choose names that clearly reveal the purpose and behavior of variables, functions, and methods. Names should be self-documenting and follow these patterns:

- **Boolean variables**: Use `is`, `has`, or `should` prefixes (e.g., `isInitialBuildSuccessful` instead of `diagnostics`)
- **Async methods**: Include action verbs that indicate the operation (e.g., `loadStorybookInfo()` instead of `storybookInfo`)  
- **Function parameters**: Use descriptive names instead of generic ones (e.g., `before, after` instead of `a, b`)
- **Test descriptions**: Avoid redundant words like "should" - prefer direct action descriptions (e.g., `"initializes"` instead of `"should initialize"`)

Example improvements:
```typescript
// Before
const diagnostics: boolean
async get storybookInfo()
function percentageDiff(a: number, b: number)

// After  
const diagnosticsEnabled: boolean
async loadStorybookInfo()
function percentageDiff(before: number, after: number)
```

Well-named code reduces the need for comments and makes the codebase more maintainable by clearly communicating intent to other developers.