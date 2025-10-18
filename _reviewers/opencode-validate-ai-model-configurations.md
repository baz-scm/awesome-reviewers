---
title: validate AI model configurations
description: When adding or modifying AI model configurations, ensure proper validation
  through both pattern-based matching and functional testing. Avoid hardcoding specific
  model IDs when existing patterns can handle multiple models generically. Always
  test model functionality before adding to production configurations.
repository: sst/opencode
label: AI
language: TypeScript
comments_count: 2
repository_stars: 28213
---

When adding or modifying AI model configurations, ensure proper validation through both pattern-based matching and functional testing. Avoid hardcoding specific model IDs when existing patterns can handle multiple models generically. Always test model functionality before adding to production configurations.

For region-specific model handling, prefer pattern-based approaches:
```typescript
// Instead of hardcoding each model:
if (isAustraliaRegion && 
  (modelID.startsWith("anthropic.claude-sonnet-4-5") || modelID.startsWith("anthropic.claude-haiku-4-5"))) {
  modelID = `au.${modelID}`
}

// Use existing patterns:
const modelRequiresPrefix = ["claude", "nova-lite", "nova-micro", "nova-pro"].some((m) => 
  modelID.includes(m))
```

For model priority lists, verify functionality before deployment:
```typescript
// Test each model before adding to priority list
const priority = ["llama3", "gemini-2.5-pro-preview", "codex-mini", "claude-sonnet-4"]
// Ensure models work beyond just the first request
```

This approach reduces maintenance overhead and prevents production issues with untested AI model configurations.