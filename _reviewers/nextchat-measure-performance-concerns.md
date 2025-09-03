---
title: Measure performance concerns
description: Before assuming performance issues exist, measure actual execution time
  and resource usage. When performance problems are confirmed, eliminate unnecessary
  operations like redundant initializations, blocking operations, or wasteful resource
  usage.
repository: ChatGPTNextWeb/NextChat
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 85721
---

Before assuming performance issues exist, measure actual execution time and resource usage. When performance problems are confirmed, eliminate unnecessary operations like redundant initializations, blocking operations, or wasteful resource usage.

Use performance measurement tools to validate concerns:

```javascript
function escapeBrackets(text: string) {
  let begin_time = performance.now();
  const pattern = /(```[\s\S]*?```|`.*?`)|\\\[([\s\S]*?[^\\])\\\]|\\\((.*?)\\\)/g;
  let res = text.replace(pattern, (match, codeBlock, squareBracket, roundBracket) => {
    // ... processing logic
  });
  let endTime = performance.now();
  console.log(`escapeBrackets, string length=${text.length}, time consumed=${endTime - begin_time} ms`);
  return res;
}
```

Common wasteful operations to eliminate:
- Re-initializing objects on every render (move initialization outside component or use useMemo)
- Performing blocking operations before user-facing actions (play audio immediately, save separately)
- Using inefficient data formats when alternatives exist (consider compressed formats over raw formats)

Modern JavaScript engines often optimize common patterns like regex compilation, but measurement reveals the actual impact rather than assumptions.