---
title: Configurable model selection
description: Avoid hard-coding model names and provider-specific configurations throughout
  the codebase. Instead, implement flexible model selection patterns that support
  runtime configuration and consistent naming conventions across different AI providers.
repository: browserbase/stagehand
label: AI
language: TypeScript
comments_count: 9
repository_stars: 16443
---

Avoid hard-coding model names and provider-specific configurations throughout the codebase. Instead, implement flexible model selection patterns that support runtime configuration and consistent naming conventions across different AI providers.

Key practices:
- Use configuration objects or environment variables instead of hard-coded model strings
- Implement consistent naming conventions for provider-specific models (e.g., "cerebras-llama-3.3-70b" instead of "llama-3.3-70b")
- Support model overrides at the function level while maintaining sensible defaults
- Remove provider-specific parameter handling from shared code paths

Example of problematic pattern:
```typescript
// Bad: Hard-coded model name
const response = await client.chat.completions.create({
  model: "gpt-4o", // Hard-coded
  messages: [...],
});

// Bad: Repetitive model specification
await stagehand.act({ action: "start game", model_name: "gpt-4o" });
await stagehand.extract({ instruction: "get price", model_name: "gpt-4o" });
```

Example of improved pattern:
```typescript
// Good: Configurable with defaults
class Stagehand {
  constructor(private defaultModel: string = "gpt-4o") {}
  
  async act(options: { action: string; modelName?: string }) {
    const model = options.modelName || this.defaultModel;
    // Use configured model
  }
}

// Good: Consistent provider naming
const modelToProviderMap: { [key in AvailableModel]: ModelProvider } = {
  "cerebras-llama-3.3-70b": "cerebras",
  "openai-gpt-4o": "openai",
};
```

This approach improves maintainability, reduces duplication, and makes model selection more flexible for different deployment scenarios.