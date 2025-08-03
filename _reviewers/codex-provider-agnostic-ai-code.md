---
title: Provider-agnostic AI code
description: Design AI integration code to be provider-agnostic, avoiding assumptions
  that all models will come from a single provider. Implement explicit handling for
  known models while maintaining fallback mechanisms for others.
repository: openai/codex
label: AI
language: TypeScript
comments_count: 2
repository_stars: 31275
---

Design AI integration code to be provider-agnostic, avoiding assumptions that all models will come from a single provider. Implement explicit handling for known models while maintaining fallback mechanisms for others.

For example, when determining model capabilities like context length:

```typescript
function maxTokensForModel(model: string): number {
  // First check if it's a known model in our registry
  if (openAiModelInfo[model]) {
    return openAiModelInfo[model].maxContextLength;
  }
  
  // Fallback to pattern-based detection for other providers
  const lower = model.toLowerCase();
  if (lower.includes("32k")) {
    return 32000;
  }
  if (lower.includes("16k")) {
    return 16000;
  }
  if (lower.includes("8k")) {
    return 8000;
  }
  if (lower.includes("4k")) {
    return 4000;
  }
  return 128000; // Default fallback
}
```

Similarly, when instantiating clients, reuse existing ones when possible rather than creating provider-specific instances that duplicate logic and may drift in configuration.