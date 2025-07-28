---
title: AI provider consistency
description: Ensure consistent patterns and configurations across all AI model providers
  to maintain code maintainability and scalability. This includes providing proper
  default configurations for all providers and minimizing provider-specific conditional
  logic that can become unwieldy as more AI models are integrated.
repository: cline/cline
label: AI
language: TSX
comments_count: 2
repository_stars: 48299
---

Ensure consistent patterns and configurations across all AI model providers to maintain code maintainability and scalability. This includes providing proper default configurations for all providers and minimizing provider-specific conditional logic that can become unwieldy as more AI models are integrated.

Key practices:
- Always define default model IDs for new AI providers
- Use unified configuration patterns rather than provider-specific if/else chains
- Apply consistent token limit handling across different providers when possible
- Design provider integrations with future model additions in mind

Example of inconsistent approach to avoid:
```typescript
// Avoid provider-specific logic scattered throughout
const maxTokens = apiConfiguration?.apiProvider === "gemini" 
    ? geminiModels[geminiDefaultModelId].maxTokens
    : anthropicModels["claude-3-7-sonnet-20250219"].maxTokens

// Instead, use a unified approach
case "sambanova":
    return getProviderData(sambanovaModels, sambanovaDefaultModelId) // Always provide default
```

This approach reduces technical debt and makes the codebase more maintainable as the number of supported AI providers grows.