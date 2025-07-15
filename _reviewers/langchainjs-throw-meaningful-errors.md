---
title: Throw meaningful errors
description: Always throw specific, actionable errors instead of returning unexpected
  values or simply logging issues. Error messages should be clear, concise, and contain
  the exact reason for failure without redundancy.
repository: langchain-ai/langchainjs
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 15004
---

Always throw specific, actionable errors instead of returning unexpected values or simply logging issues. Error messages should be clear, concise, and contain the exact reason for failure without redundancy.

Consider these practices:

1. When a function can't perform its task, throw an error rather than returning a default value:
```typescript
// Bad
_combineLLMOutput(): Record<string, any> | undefined {
  return [];  // Returns unexpected empty array
}

// Good
_combineLLMOutput(): Record<string, any> | undefined {
  throw new Error("AzureMLChatOnlineEndpoint._combineLLMOutput called, but is not implemented.");
}
```

2. Avoid redundant error prefixes that will be repeated in logs:
```typescript
// Bad - creates redundant messages
if (!response.ok) {
  throw new Error(`Error authenticating with Reddit: ${response.statusText}`);
}

// Good - concise and clear
if (!response.ok) {
  throw new Error(response.statusText);
}
```

3. Propagate errors instead of just logging them to allow proper handling up the call stack:
```typescript
// Bad - swallows the error
try {
  await this.collection.deleteMany({});
} catch (error) {
  console.log("Error clearing sessions:", error);
}

// Good - allows callers to handle the error
try {
  await this.collection.deleteMany({});
} catch (error) {
  console.error("Error clearing sessions:", error);
  throw error; // Re-throw or throw a more specific error
}
```

4. Preserve error structures expected by error handling mechanisms:
```typescript
// Bad - overwrites properties needed for retry logic
(error as any).details = { /* ... */ };

// Good - maintains expected structure
(error as any).response = res;
```

Well-designed error handling improves debugging efficiency and creates a more robust application.
