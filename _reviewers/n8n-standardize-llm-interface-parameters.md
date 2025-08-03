---
title: Standardize LLM interface parameters
description: 'Maintain consistent parameter names and interface patterns across LLM
  implementations to improve maintainability and prevent integration issues. This
  includes:'
repository: n8n-io/n8n
label: AI
language: TypeScript
comments_count: 6
repository_stars: 122978
---

Maintain consistent parameter names and interface patterns across LLM implementations to improve maintainability and prevent integration issues. This includes:

1. Use standard parameter names across all LLM integrations (e.g., 'maxTokens' instead of 'maxTokensToSample')
2. Check for specific required capabilities rather than assuming implementation details
3. Use consistent property access patterns for LLM responses

Example:
```typescript
// INCORRECT
if (!llm.bindTools) {
  throw new LLMServiceError("LLM doesn't support binding tools");
}
const tokens = llmOutput?.tokenUsage?.completionTokens;

// CORRECT
if (typeof llm.withStructuredOutput !== 'function') {
  throw new LLMServiceError("LLM doesn't support structured output");
}
const tokens = llmResult?.llmOutput?.tokenUsage?.completionTokens;
```

This standardization:
- Reduces confusion and errors when working with multiple LLM implementations
- Makes code more maintainable and easier to understand
- Simplifies integration of new LLM providers
- Enables consistent error handling and capability checking