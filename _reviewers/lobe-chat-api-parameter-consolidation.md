---
title: API parameter consolidation
description: When designing API functions with multiple parameters, consolidate optional
  or related parameters into a single options object to improve extensibility and
  maintainability. This pattern prevents function signatures from becoming unwieldy
  and allows for easier future parameter additions without breaking changes.
repository: lobehub/lobe-chat
label: API
language: TypeScript
comments_count: 5
repository_stars: 65138
---

When designing API functions with multiple parameters, consolidate optional or related parameters into a single options object to improve extensibility and maintainability. This pattern prevents function signatures from becoming unwieldy and allows for easier future parameter additions without breaking changes.

Key principles:
- When a function has 3 or more parameters, move non-essential parameters into an options object
- Group related parameters together (e.g., callbacks and configuration options)
- Use existing utility functions instead of manual implementations for common operations

Example of good parameter consolidation:
```typescript
// Before: Multiple separate parameters
export const QwenAIStream = (
  stream: Stream<OpenAI.ChatCompletionChunk>,
  callbacks?: ChatStreamCallbacks,
  inputStartAt?: number,
)

// After: Consolidated into options object
export const QwenAIStream = (
  stream: Stream<OpenAI.ChatCompletionChunk>,
  options?: {
    callbacks?: ChatStreamCallbacks;
    inputStartAt?: number;
  }
)
```

Example of using utility functions:
```typescript
// Before: Manual URL construction
const avatarUrl = fileEnv.S3_PUBLIC_DOMAIN + '/' + filePath;

// After: Using utility function
const avatarUrl = await ctx.fileService.getFullFileUrl(filePath);

// Before: Manual URL joining
endpointUrl: instance.baseURL + '/' + payload.model

// After: Using urlJoin utility
endpointUrl: urlJoin(instance.baseURL, payload.model)
```

This approach makes APIs more maintainable, reduces the likelihood of bugs from manual implementations, and provides a clear upgrade path for future enhancements.