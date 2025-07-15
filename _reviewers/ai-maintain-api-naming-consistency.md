---
title: Maintain API naming consistency
description: When working with AI model interfaces and result objects, ensure consistent
  property naming across related components. The AI ecosystem involves multiple providers
  and model types, making naming consistency crucial for maintainable code.
repository: vercel/ai
label: AI
language: TypeScript
comments_count: 5
repository_stars: 15590
---

When working with AI model interfaces and result objects, ensure consistent property naming across related components. The AI ecosystem involves multiple providers and model types, making naming consistency crucial for maintainable code.

For example, use the same property name consistently when accessing similar data from model results:

```javascript
// INCORRECT
console.log('Responses:', result.responses);

// CORRECT
console.log('Response:', result.response);
```

This consistency should extend across different AI capabilities (text generation, transcription, embedding, etc.) to create a cohesive developer experience. Inconsistent naming patterns lead to:

1. Developer confusion when switching between model types
2. Harder code maintenance as the application grows
3. Bugs from incorrectly accessing properties with similar purposes but different names

When designing AI interfaces or extending existing ones, audit the naming patterns of related components and align new additions with established conventions. This is particularly important when working with response objects from different AI providers that may use varying terminology for similar concepts.