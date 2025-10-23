---
title: separate model-specific configuration
description: Avoid mixing model-specific features with provider-level configuration
  or hard-coding model-specific logic in generic handlers. This creates architectural
  debt and maintenance burden as new AI models are added to the system.
repository: dyad-sh/dyad
label: AI
language: TypeScript
comments_count: 2
repository_stars: 16903
---

Avoid mixing model-specific features with provider-level configuration or hard-coding model-specific logic in generic handlers. This creates architectural debt and maintenance burden as new AI models are added to the system.

Model-specific features (like thinking modes, specialized parameters, or model-unique behaviors) should be handled through dedicated model configuration layers rather than being embedded in provider settings or generic request handlers.

Example of what to avoid:
```typescript
// DON'T: Model-specific config in provider schema
export const ProviderSettingSchema = z.object({
  apiKey: SecretSchema.optional(),
  // Model-specific feature mixed with provider config
  enableFlashThinking: z.boolean().optional(),
});

// DON'T: Hard-coded model logic in generic handlers
if (selectedProviderId === "google" && selectedModelName === "flash-2.5") {
  includeGoogleThoughts = settings.enableFlashThinking;
}
```

Instead, design model configuration to be modular and keep provider settings focused on provider-level concerns like authentication and endpoints. This approach scales better as new models with unique features are integrated.