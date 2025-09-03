---
title: Model specification accuracy
description: Ensure AI model configurations accurately reflect official specifications
  and avoid hardcoded assumptions. Model parameters, token limits, capabilities, and
  naming should match vendor documentation rather than using generic defaults.
repository: lobehub/lobe-chat
label: AI
language: TypeScript
comments_count: 12
repository_stars: 65138
---

Ensure AI model configurations accurately reflect official specifications and avoid hardcoded assumptions. Model parameters, token limits, capabilities, and naming should match vendor documentation rather than using generic defaults.

Key practices:
- Verify token counts include both input and output limits (e.g., `tokens: maxInput + maxOutput`)
- Avoid hardcoded parameter defaults that don't apply universally (like `default: 0.8` for strength)
- Use consistent naming conventions (e.g., "Imagen 4" with spaces, remove "Instruct" for base models)
- Add "Preview" or "Beta" labels for experimental models
- Remove deprecated models only when official end-of-life dates are announced
- Cross-reference specifications with official API documentation

Example of proper model configuration:
```typescript
{
  description: 'Gemini 2.5 Flash 是 Google 最先进的主力模型',
  displayName: 'Gemini 2.5 Flash', // Clear, consistent naming
  id: 'google/gemini-2.5-flash',
  contextWindowTokens: 1_048_576, // Verified against official docs
  maxOutput: 65_535, // Separate input/output limits
  // No hardcoded parameter defaults
}
```

This prevents user confusion, billing errors, and ensures reliable model behavior across different AI providers.