---
title: Co-locate related code
description: 'Place related code segments together, particularly when they perform
  related operations or have shared dependencies. This includes:


  1. Comments should be co-located with the code they describe'
repository: facebook/react
label: Code Style
language: Javascript
comments_count: 2
repository_stars: 236926
---

Place related code segments together, particularly when they perform related operations or have shared dependencies. This includes:

1. Comments should be co-located with the code they describe
2. Function calls that operate on the same data should be grouped
3. Operations that may trigger related side-effects should be kept together

This practice improves readability, maintainability, and helps prevent bugs when code is modified.

Example:
```javascript
// Prefer this:
if (__DEV__) {
  // Comment explaining the initialization
  const init = initializeElement.bind(null, response, element);
  blockedChunk.then(init, init);
}

// Instead of separating related operations:
if (__DEV__) {
  const init = initializeElement.bind(null, response, element);
  blockedChunk.then(init, init);
}
// Comment explaining initialization (misplaced)
```

When moving code during refactoring, always ensure that related comments, operations, and side-effects stay together to maintain logical coherence.