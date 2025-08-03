---
title: Standardize AI model interfaces
description: When implementing AI model integrations, maintain consistent interfaces
  and proper type definitions across different providers. This ensures compatibility,
  prevents runtime errors, and simplifies maintenance.
repository: continuedev/continue
label: AI
language: TypeScript
comments_count: 5
repository_stars: 27819
---

When implementing AI model integrations, maintain consistent interfaces and proper type definitions across different providers. This ensures compatibility, prevents runtime errors, and simplifies maintenance.

Key guidelines:
1. Define explicit interfaces for model-specific features
2. Isolate provider-specific logic in dedicated classes
3. Use proper type definitions for model responses
4. Maintain consistent parameter naming across providers

Example of proper implementation:

```typescript
// Define shared interface
interface ModelProvider {
  embed(chunks: string[], task: EmbeddingTasks): Promise<number[][]>;
  chat(messages: ChatMessage[], options: ChatOptions): AsyncGenerator<string>;
}

// Implement provider-specific class
class DeepSeekProvider implements ModelProvider {
  // Extend base types for provider-specific features
  interface DeepSeekMessage extends ChatMessage {
    reasoning_content?: string;
  }

  // Implement shared interface with provider-specific logic
  async embed(chunks: string[], task: EmbeddingTasks): Promise<number[][]> {
    // Provider-specific implementation
  }
}
```

This approach:
- Prevents interface breaking changes
- Makes provider-specific features explicit
- Ensures type safety across the application
- Simplifies adding new model providers