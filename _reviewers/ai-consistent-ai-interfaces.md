---
title: Consistent AI interfaces
description: Maintain consistent naming patterns and parameter structures across AI
  provider implementations. This makes the SDK more intuitive and reduces developer
  friction when switching between different AI models or providers.
repository: vercel/ai
label: AI
language: Markdown
comments_count: 2
repository_stars: 15590
---

Maintain consistent naming patterns and parameter structures across AI provider implementations. This makes the SDK more intuitive and reduces developer friction when switching between different AI models or providers.

Key practices:
- Use `.response` instead of `.rawResponse` for provider API responses
- Place provider-specific options under `providerOptions` parameter
- Ensure documentation examples accurately reflect the actual API capabilities and valid model identifiers

Example:
```ts
// Preferred approach
const { response } = await embed({
  providerOptions: {
    // Provider-specific options here
  }
});

// Instead of
const { rawResponse } = await embed({
  // Mixing provider-specific options at the top level
});
```

When adding examples for AI providers, always verify that model identifiers are valid for the specific provider (e.g., using 'scribe_v1' for ElevenLabs transcription models rather than invalid identifiers).