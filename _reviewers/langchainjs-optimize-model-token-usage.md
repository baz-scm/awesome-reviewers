---
title: Optimize model token usage
description: 'Implement token-efficient patterns when working with AI models to optimize
  costs and performance. Key practices include:


  1. Batch identical prompts into single API calls where supported'
repository: langchain-ai/langchainjs
label: AI
language: TypeScript
comments_count: 5
repository_stars: 15004
---

Implement token-efficient patterns when working with AI models to optimize costs and performance. Key practices include:

1. Batch identical prompts into single API calls where supported
2. Leverage provider-specific features for token efficiency
3. Use appropriate token counting methods for accurate estimation

Example of efficient batching with OpenAI:

```typescript
// Inefficient: Multiple separate calls
const results = await Promise.all(
  inputs.map(input => model.generate(input))
);

// Efficient: Single batched call
const results = await model.generate(
  [promptValue], 
  { n: inputs.length }  // OpenAI charges input tokens only once
);

// For accurate token counting:
const tokenCount = await model.getNumTokensFromMessages(messages);
```

This approach can significantly reduce costs, especially for use cases with high input token counts relative to output. Different providers may offer varying batching capabilities - consult their documentation for optimal usage patterns.
