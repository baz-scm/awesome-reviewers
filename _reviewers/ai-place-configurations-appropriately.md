---
title: Place configurations appropriately
description: Configuration options should be organized based on their nature and scope
  of use. Place model-specific configurations in constructor parameters or config
  objects rather than in general settings objects that might be shared across models.
  Additionally, standardized settings should be consistent across providers and not
  duplicated in provider-specific options.
repository: vercel/ai
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 15590
---

Configuration options should be organized based on their nature and scope of use. Place model-specific configurations in constructor parameters or config objects rather than in general settings objects that might be shared across models. Additionally, standardized settings should be consistent across providers and not duplicated in provider-specific options.

This organization improves code maintainability and prevents confusion about where settings should be defined or accessed.

```typescript
// GOOD: Model-specific config in constructor parameters
constructor(
  modelId: OpenAICompatibleChatModelId,
  settings: OpenAICompatibleChatSettings,
  config: OpenAICompatibleChatConfig & {
    defaultObjectGenerationMode?: 'json' | 'tool' | undefined;
  }
) { ... }

// BAD: Model-specific config in settings
export interface OpenAICompatibleChatSettings {
  user?: string;
  defaultObjectGenerationMode?: 'json' | 'tool' | undefined; // Should be in config instead
}

// GOOD: Standardized settings not duplicated in provider options
// For settings like 'voice' that are standardized across providers
speech.generate("Hello world", {
  voice: "alloy",  // Top-level standardized setting
});

// BAD: Duplicating standardized settings in provider options
speech.generate("Hello world", {
  providerOptions: {
    openai: {
      voice: "alloy",  // Duplicated standardized setting
    }
  }
});
```

For common settings that apply across different providers (like 'voice' for speech models or 'language' for transcription), define them as top-level options rather than duplicating them in each provider's specific options.