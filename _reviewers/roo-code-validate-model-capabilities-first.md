---
title: Validate model capabilities first
description: 'Always validate AI model capabilities and configurations before attempting
  to use them. This includes checking:


  1. Feature support (e.g., images, embeddings)'
repository: RooCodeInc/Roo-Code
label: AI
language: TypeScript
comments_count: 3
repository_stars: 17288
---

Always validate AI model capabilities and configurations before attempting to use them. This includes checking:

1. Feature support (e.g., images, embeddings)
2. Model-specific parameters (e.g., dimensions, context windows)
3. Model availability and correct configuration

Example:
```typescript
// Before using model features, validate capabilities
const provider = await client.providerRef.deref();
const modelCapabilities = {
  supportsImages: provider?.apiHandler?.getModel()?.info?.supportsImages ?? false,
  supportedDimensions: [768, 1536, 3072],
  isModelAvailable: Boolean(routerModels[provider]?.[modelId])
};

// Use capabilities to make decisions
const imagesToInclude = modelCapabilities.supportsImages ? allImages : [];
if (!modelCapabilities.isModelAvailable) {
  throw new Error(`Model ${modelId} is not available`);
}
```

This prevents runtime errors, improves reliability, and ensures optimal resource usage. It's particularly important in AI applications where different models may have varying capabilities and requirements.