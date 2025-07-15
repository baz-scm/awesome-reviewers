---
title: Verify assertions properly
description: 'Ensure test assertions correctly validate the intended behavior by:


  1. **Awaiting promise assertions** when testing async code:

  ```javascript

  // PROBLEMATIC: Test may pass even if promise never resolves'
repository: oven-sh/bun
label: Testing
language: JavaScript
comments_count: 3
repository_stars: 79093
---

Ensure test assertions correctly validate the intended behavior by:

1. **Awaiting promise assertions** when testing async code:
```javascript
// PROBLEMATIC: Test may pass even if promise never resolves
expect(promise).resolves.toBe(expectedValue);

// CORRECT: Properly wait for and validate promise resolution
await expect(promise).resolves.toBe(expectedValue);
// OR
return expect(promise).resolves.toBe(expectedValue);
```

2. **Comparing appropriate values** when testing transformations:
```javascript
// PROBLEMATIC: Comparing decompressed output to compressed input
expect(decompressedBuffer).toEqual(compressedBuffer);

// CORRECT: Verifying the transformation worked as expected
expect(decompressedBuffer.toString()).toEqual(originalInputString);
```

Understanding your testing framework's behavior is important - some frameworks may handle certain assertions differently (e.g., in some environments `expect(...).resolves` might implicitly await).

Tests should validate that functions behave as expected, not just that they run without errors. Always ask: "Is this assertion actually testing what I intend to test?"