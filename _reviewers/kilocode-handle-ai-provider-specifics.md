---
title: Handle AI provider specifics
description: Different AI providers and models have unique requirements for input
  processing, output filtering, and API parameters that must be implemented correctly.
  When working with AI APIs, research and implement provider-specific handling rather
  than assuming uniform behavior across all providers.
repository: kilo-org/kilocode
label: AI
language: TypeScript
comments_count: 3
repository_stars: 7302
---

Different AI providers and models have unique requirements for input processing, output filtering, and API parameters that must be implemented correctly. When working with AI APIs, research and implement provider-specific handling rather than assuming uniform behavior across all providers.

Key considerations:
- **Input filtering**: Some providers require filtering of thinking tags or special content (e.g., `filterThinkingTags(block.text)` for certain models)
- **Parameter requirements**: Certain providers mandate specific parameters like `max_tokens` to prevent output truncation, especially for models like DeepSeek R1
- **Specialized parsing**: Complex AI responses may need custom JSON parsing logic beyond standard utilities when dealing with malformed LLM outputs

Example implementation:
```typescript
// Provider-specific parameter handling
const requestOptions = {
    model: model.id,
    messages: openAiMessages,
    max_tokens: maxOutputTokens, // Required by Fireworks API
    // ... other provider-specific params
}

// Provider-specific content filtering
const processedContent = isSpecialModel 
    ? filterThinkingTags(block.text)
    : block.text
```

Before implementing generic solutions, verify whether the target AI provider has documented requirements or behavioral differences that need accommodation.