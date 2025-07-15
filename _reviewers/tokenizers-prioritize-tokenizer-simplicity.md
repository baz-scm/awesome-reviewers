---
title: Prioritize tokenizer simplicity
description: 'When implementing AI model components like tokenizers, favor simplicity
  over rarely-used features that significantly increase code complexity. This is especially
  important for performance-critical paths in machine learning pipelines. Consider
  removing or deferring implementation of features that:'
repository: huggingface/tokenizers
label: AI
language: TypeScript
comments_count: 2
repository_stars: 9868
---

When implementing AI model components like tokenizers, favor simplicity over rarely-used features that significantly increase code complexity. This is especially important for performance-critical paths in machine learning pipelines. Consider removing or deferring implementation of features that:
1. Require complex argument parsing
2. Are used only in specialized cases
3. Introduce significant maintenance burden

Example:
```typescript
// AVOID: Complex implementation with rarely-used features
let encodeBatch = promisify(tokenizer.encodeBatch.bind(tokenizer));
var output = await encodeBatch(
    [["Hello, y'all!", "How are you 😁 ?"], ["Hello to you too!", "I'm fine, thank you!"]]
);

// BETTER: Simplified implementation focusing on core functionality
var output = await tokenizer.encodeBatch(["Hello, y'all!", "How are you 😁 ?"]);
```

This approach helps maintain performance in AI inference paths while keeping the codebase maintainable. Features can always be added later when there's a clear need and sufficient time for proper implementation.