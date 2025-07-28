---
title: Test all variations
description: Ensure comprehensive test coverage by testing all behavioral variations,
  configuration options, and edge cases rather than just single scenarios. When adding
  new functionality, preserve existing tests and add new ones to cover both old and
  new behaviors.
repository: prettier/prettier
label: Testing
language: Other
comments_count: 2
repository_stars: 50772
---

Ensure comprehensive test coverage by testing all behavioral variations, configuration options, and edge cases rather than just single scenarios. When adding new functionality, preserve existing tests and add new ones to cover both old and new behaviors.

For example, when modifying a function to support both synchronous and asynchronous behavior, maintain separate tests for each:

```javascript
// Keep existing sync test
"foo-parser": {
  preprocess: (text) => `preprocessed:${text}`,

// Add new async test  
"foo-parser-async": {
  preprocess: (text) => Promise.resolve(`preprocessed:${text}`),
```

Similarly, when implementing features with configuration options, test multiple settings rather than just defaults:

```javascript
// Test different quoteProps options
{"quoteProps": "consistent"}
{"quoteProps": "as-needed"} 
{"quoteProps": "preserve"}
```

This approach prevents regressions and ensures robust functionality across all supported use cases.