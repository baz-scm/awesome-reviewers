---
title: AI model integration patterns
description: When integrating with AI models and LLMs, structure your code to properly
  handle model responses, separate concerns between layers, and implement robust failure
  detection mechanisms.
repository: google-gemini/gemini-cli
label: AI
language: TypeScript
comments_count: 10
repository_stars: 65062
---

When integrating with AI models and LLMs, structure your code to properly handle model responses, separate concerns between layers, and implement robust failure detection mechanisms.

**Core Principles:**

1. **Separate raw model data from presentation logic**: Core libraries should emit raw model responses (like finish reasons, confidence scores) while UI layers handle user-facing formatting and messages. This ensures library consumers aren't forced to receive UI-specific content.

2. **Design schemas with proper field ordering**: When using structured generation with AI models, place reasoning fields before conclusion fields in your schema. This encourages the model to think through the problem before providing final answers, improving response quality.

3. **Implement systematic failure detection**: For long-running AI interactions, implement detection mechanisms for common failure modes like repetitive loops or unproductive states. Use dynamic check intervals based on confidence levels rather than fixed intervals.

4. **Handle streaming and incomplete responses safely**: When processing streaming AI output, use permissive parsing that can handle incomplete or improperly formatted content, prioritizing safe rendering over strict specification compliance.

**Example Implementation:**

```typescript
// Good: Core library emits raw finish reason
if (finishReason && finishReason !== FinishReason.STOP) {
  yield {
    type: GeminiEventType.Finished,
    value: finishReason  // Raw enum value
  };
}

// Good: UI layer handles user-facing messages
const finishReasonMessages: Record<string, string> = {
  'MAX_TOKENS': '⚠️ Response truncated due to token limits.',
  'SAFETY': '⚠️ Response stopped due to safety reasons.'
};

// Good: Schema with reasoning before conclusion
const schema = {
  type: Type.OBJECT,
  properties: {
    reasoning: {
      type: Type.STRING,
      description: 'Your reasoning process'
    },
    confidence: {
      type: Type.NUMBER,
      description: 'Confidence level 0.0-1.0'
    }
  }
};
```

This approach ensures maintainable, robust AI integrations that can handle the unpredictable nature of model responses while providing clean separation of concerns.