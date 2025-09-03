---
title: Account for model variations
description: When implementing features that interact with AI models, consider the
  behavioral differences between various models and adjust parameters accordingly.
  Different AI models have distinct characteristics such as output speed, token generation
  patterns, and response formats that can significantly impact user experience.
repository: lobehub/lobe-chat
label: AI
language: TSX
comments_count: 2
repository_stars: 65138
---

When implementing features that interact with AI models, consider the behavioral differences between various models and adjust parameters accordingly. Different AI models have distinct characteristics such as output speed, token generation patterns, and response formats that can significantly impact user experience.

For example, streaming chat interfaces need different auto-scroll thresholds for different models:

```typescript
// Consider model output characteristics
const getScrollThreshold = (modelType: string) => {
  // Fast models (GPT-3.5, Sonnet, Groq) output in bursts
  if (modelType.includes('gpt-3.5') || modelType.includes('sonnet')) {
    return 80; // Higher threshold for burst output
  }
  // Slower models (Gemini) output character by character  
  return 50; // Lower threshold for steady output
};

<Virtuoso
  atBottomThreshold={getScrollThreshold(currentModel)}
  // ... other props
/>
```

This approach prevents common issues like auto-scroll failing when fast models output multiple lines simultaneously, or performance problems when not optimizing for model-specific behaviors. Always test with different model types to ensure consistent user experience across various AI providers.