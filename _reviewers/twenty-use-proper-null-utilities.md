---
title: Use proper null utilities
description: Use dedicated null checking utilities like `isDefined` or `isUndefinedOrNull`
  instead of generic type coercion functions like `Boolean()`. Prefer `undefined`
  over empty strings or `null` as default values to maintain type safety and prevent
  runtime errors.
repository: twentyhq/twenty
label: Null Handling
language: TSX
comments_count: 3
repository_stars: 35477
---

Use dedicated null checking utilities like `isDefined` or `isUndefinedOrNull` instead of generic type coercion functions like `Boolean()`. Prefer `undefined` over empty strings or `null` as default values to maintain type safety and prevent runtime errors.

Avoid patterns like:
```typescript
// Problematic
const isStreaming = Boolean(agentStreamingMessage) && streamData === agentStreamingMessage;
fieldName = '',  // empty string default
sourceHandle: null,  // explicit null

// Better
const isStreaming = isDefined(agentStreamingMessage) && streamData === agentStreamingMessage;
fieldName,  // undefined default
sourceHandle: DEFAULT_SOURCE_HANDLE_ID,  // meaningful default
```

This approach provides clearer intent, better type safety, and reduces the likelihood of runtime errors caused by unexpected falsy values.