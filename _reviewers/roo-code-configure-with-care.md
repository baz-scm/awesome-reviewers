---
title: Configure with care
description: 'Always validate configuration values before use, provide sensible defaults,
  and centralize constants in shared modules. When implementing configuration handling:'
repository: RooCodeInc/Roo-Code
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 17288
---

Always validate configuration values before use, provide sensible defaults, and centralize constants in shared modules. When implementing configuration handling:

1. Use explicit undefined checks instead of truthy checks to properly handle zero values:
```typescript
// Incorrect: Will skip valid zero values
if (configuration.commandExecutionTimeout) {
  // Handle timeout
}

// Correct: Properly handles zero values
if (configuration.commandExecutionTimeout !== undefined) {
  // Handle timeout
}
```

2. Apply bounds checking for numerical values to ensure they're within acceptable ranges:
```typescript
// Validate within reasonable bounds
const maxImagesPerResponse = Math.max(1, Math.min(100, state?.mcpMaxImagesPerResponse ?? 20));
const maxImageSizeMB = Math.max(0.1, Math.min(50, state?.mcpMaxImageSizeMB ?? 10));
```

3. Parse or validate types for configuration fields to prevent propagating invalid values:
```typescript
// Ensure configuration value is a valid number
this.modelDimension = typeof config.modelDimension === 'number' && !isNaN(config.modelDimension) 
  ? config.modelDimension 
  : DEFAULT_MODEL_DIMENSION;
```

4. Extract repeated literal values into named constants to maintain consistency:
```typescript
// Define in a shared constants file
export const DEFAULT_CLAUDE_CODE_MAX_OUTPUT_TOKENS = 8000;

// Use the constant throughout the codebase
return settings.claudeCodeMaxOutputTokens || DEFAULT_CLAUDE_CODE_MAX_OUTPUT_TOKENS;
```

Proper configuration handling prevents subtle bugs, improves maintainability, and makes your code more resilient to external changes.