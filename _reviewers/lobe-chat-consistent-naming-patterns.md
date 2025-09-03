---
title: consistent naming patterns
description: Maintain consistent naming conventions within related groups of identifiers.
  When naming related variables, functions, or constants, use the same naming pattern
  and style to improve code readability and maintainability.
repository: lobehub/lobe-chat
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 65138
---

Maintain consistent naming conventions within related groups of identifiers. When naming related variables, functions, or constants, use the same naming pattern and style to improve code readability and maintainability.

Apply consistent patterns for:
- **Environment variables**: Related config variables should follow the same naming structure
- **Database fields**: Use consistent naming style within the same table or related tables  
- **Function parameters**: Related parameters should use similar naming patterns
- **Configuration objects**: Distinguish between contexts (snake_case for config files, camelCase for code variables)
- **Display names**: Preserve established conventions for well-known identifiers

Example from discussions:
```typescript
// Good: Consistent environment variable naming
FEISHU_APP_ID: process.env.FEISHU_APP_ID,
FEISHU_APP_SECRET: process.env.FEISHU_APP_SECRET,

// Good: Consistent database field naming  
emailVerifiedAt: timestamptz('email_verified_at'),
clerkCreatedAt: timestamptz('clerk_created_at'),

// Good: Specific, descriptive function names
initAgentRuntimeWithUserPayload() // Clear object and action

// Good: Context-appropriate naming
// Config files use snake_case
embedding_model: DEFAULT_FILE_EMBEDDING_MODEL_ITEM,
// Code variables use camelCase  
embeddingModel: config.embedding_model,
```

This consistency reduces cognitive load when reading code and makes the codebase more predictable for developers.