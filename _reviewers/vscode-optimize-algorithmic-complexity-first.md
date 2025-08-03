---
title: Optimize algorithmic complexity first
description: 'When implementing algorithms, prioritize reducing computational complexity
  before adding special cases or optimizing for specific scenarios. Key practices:'
repository: microsoft/vscode
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 174887
---

When implementing algorithms, prioritize reducing computational complexity before adding special cases or optimizing for specific scenarios. Key practices:

1. Identify and eliminate O(n²) operations, especially nested loops and repeated array operations
2. Use appropriate data structures based on access patterns
3. Combine multiple passes into single operations where possible

Example - Converting O(n²) to O(n):

```typescript
// Poor: O(n²) complexity with multiple array operations
selections = selections.filter((s, idx, arr) => {
    return arr.map(sel => sel.endLineNumber)
              .indexOf(s.endLineNumber) === idx;
});

// Better: O(n) complexity with single pass
const seen = new Set();
const uniqueSelections = [];
for (const selection of selections) {
    if (!seen.has(selection.endLineNumber)) {
        seen.add(selection.endLineNumber);
        uniqueSelections.push(selection);
    }
}
```

When using Set operations, ensure object identity works as expected for your data type. For complex objects like URIs, implement custom equality comparisons or use appropriate key extraction.