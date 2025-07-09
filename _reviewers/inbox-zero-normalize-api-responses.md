---
title: Normalize API responses
description: 'Design APIs to return consistent response structures across different
  data sources or providers. Normalize responses at the API layer rather than handling
  provider-specific format differences in client components. This approach:'
repository: elie222/inbox-zero
label: API
language: TSX
comments_count: 4
repository_stars: 8267
---

Design APIs to return consistent response structures across different data sources or providers. Normalize responses at the API layer rather than handling provider-specific format differences in client components. This approach:

1) Maintains type safety by ensuring predictable response shapes
2) Simplifies client components by removing conditional format handling
3) Creates a clean abstraction layer for supporting multiple providers

For example, instead of handling different message formats in UI components:

```typescript
// Client-side format handling (AVOID)
const subject = "headers" in firstMessage 
  ? firstMessage.headers.subject 
  : firstMessage.subject;
const date = "headers" in firstMessage
  ? firstMessage.headers.date
  : firstMessage.receivedAt;
```

Normalize in your API controller/service layer:

```typescript
// Server-side normalization (RECOMMENDED)
export function normalizeMessageResponse(message) {
  // Creates a unified structure regardless of provider
  return {
    id: message.id,
    subject: getMessageSubject(message),
    date: getMessageDate(message),
    snippet: getMessageSnippet(message),
    // Other normalized fields
  };
}

// Helper functions handle provider-specific logic
function getMessageSubject(message) {
  return message.headers?.subject || message.subject || "";
}

function getMessageDate(message) {
  return message.headers?.date || message.receivedAt || new Date();
}
```

This pattern is especially valuable for multi-provider systems where different APIs return structurally different responses for similar data.