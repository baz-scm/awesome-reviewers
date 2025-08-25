---
title: Optimize algorithmic efficiency
description: Always consider the computational complexity of your algorithms and leverage
  efficient built-in methods when available. Look for opportunities to reduce time
  complexity and avoid unnecessary operations like redundant loops or object creation.
repository: block/goose
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 19037
---

Always consider the computational complexity of your algorithms and leverage efficient built-in methods when available. Look for opportunities to reduce time complexity and avoid unnecessary operations like redundant loops or object creation.

Common inefficiencies to watch for:
- Using nested iterations when a single pass with a data structure (Map, Set) would suffice
- Creating intermediate objects or strings when built-in method parameters can achieve the same result
- Implementing manual searches when optimized built-in methods exist

Examples of improvements:

**Before (O(n^2) deduplication):**
```javascript
promptParams.forEach((promptParam) => {
  if (!allParams.some((param) => param.key === promptParam.key)) {
    allParams.push(promptParam);
  }
});
```

**After (O(n) with Map):**
```javascript
const paramMap = new Map(allParams.map(p => [p.key, p]));
promptParams.forEach(p => paramMap.set(p.key, p));
const allParams = Array.from(paramMap.values());
```

**Before (unnecessary string creation):**
```javascript
const beforeCursor = text.slice(0, cursorPosition);
const lastAtIndex = beforeCursor.lastIndexOf('@');
```

**After (direct method usage):**
```javascript
const lastAtIndex = text.lastIndexOf('@', cursorPosition - 1);
```