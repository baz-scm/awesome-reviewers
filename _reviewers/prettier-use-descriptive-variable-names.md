---
title: Use descriptive variable names
description: Choose variable and function names that clearly communicate their purpose,
  type, and context. Avoid abbreviations, overly generic terms, and names that could
  be confused for different types.
repository: prettier/prettier
label: Naming Conventions
language: JavaScript
comments_count: 8
repository_stars: 50772
---

Choose variable and function names that clearly communicate their purpose, type, and context. Avoid abbreviations, overly generic terms, and names that could be confused for different types.

Key principles:
- **Communicate intent**: Use `array` instead of `xs`, `whitespaceCharacters` instead of `characters`
- **Indicate type when ambiguous**: Use `shouldCache` for booleans instead of `cache`, `clonedNode` instead of `clone` (which sounds like a function)
- **Be appropriately specific**: Use `createCachedSearchFunction` instead of the too-generic `createCachedFunction`, `isPrevNodeMarkdownlintComment` instead of `isPrevNodeSpecificComment`
- **Include context in method names**: Use `splitByContinuousWhitespace` instead of just `split`

Example improvements:
```javascript
// Before: unclear and generic
function chunk(xs, chunkSize) { ... }
const cache = new Map();
function createCachedFunction(function_) { ... }

// After: descriptive and clear
function chunk(array, size) { ... }
const shouldCache = true;
function createCachedSearchFunction(searchFunction) { ... }
```

This approach makes code self-documenting and reduces the cognitive load for other developers reading and maintaining the code.