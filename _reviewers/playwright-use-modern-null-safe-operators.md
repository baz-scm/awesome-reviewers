---
title: Use modern null-safe operators
description: Prefer optional chaining (`?.`) and nullish coalescing (`??`) operators
  over verbose null checks and ternary expressions. These modern JavaScript operators
  provide cleaner, more readable code while preventing runtime errors from null or
  undefined values.
repository: microsoft/playwright
label: Null Handling
language: TSX
comments_count: 3
repository_stars: 76113
---

Prefer optional chaining (`?.`) and nullish coalescing (`??`) operators over verbose null checks and ternary expressions. These modern JavaScript operators provide cleaner, more readable code while preventing runtime errors from null or undefined values.

Instead of explicit null checks:
```javascript
// Avoid
const annotations = item.testCase ? [...item.testCase.annotations, ...item.testCase.results.flatMap(r => r.annotations)] : [];

// Prefer
const annotations = item.testCase?.results[0] ? [...item.testCase.annotations, ...item.testCase.results[0].annotations] : [];
```

For array access and method calls, use optional chaining with nullish coalescing:
```javascript
// Avoid
annotations.push(...test.results[selectedResultIndex].annotations);

// Prefer  
annotations.push(...test.results[selectedResultIndex]?.annotations ?? []);
```

This approach reduces boilerplate code, improves readability, and provides built-in null safety without sacrificing functionality.