---
title: Handle AI operation failures
description: Always implement proper error handling for AI service operations. AI
  services can fail due to rate limiting, network issues, or service outages. Wrap
  AI service calls in try-catch blocks to gracefully handle potential failures, log
  relevant error information, and provide appropriate fallbacks.
repository: elie222/inbox-zero
label: AI
language: TypeScript
comments_count: 4
repository_stars: 8267
---

Always implement proper error handling for AI service operations. AI services can fail due to rate limiting, network issues, or service outages. Wrap AI service calls in try-catch blocks to gracefully handle potential failures, log relevant error information, and provide appropriate fallbacks.

```typescript
// ❌ Without error handling
const result = await chatCompletionObject({
  userAi: user,
  system,
  prompt,
  schema,
  userEmail: user.email,
  usageLabel: "AI Operation",
});

return result.object;

// ✅ With proper error handling
try {
  const result = await chatCompletionObject({
    userAi: user,
    system,
    prompt,
    schema,
    userEmail: user.email,
    usageLabel: "AI Operation",
  });
  
  logger.trace("Output", { result });
  
  return result.object;
} catch (error) {
  logger.error("AI operation failed", { error });
  return fallbackValue; // Return a sensible default
}
```

This pattern ensures that AI-dependent features degrade gracefully when AI services are unavailable, preventing unhandled exceptions from propagating and disrupting user experience. Consider defining standardized error handling functions for common AI operation patterns in your codebase.