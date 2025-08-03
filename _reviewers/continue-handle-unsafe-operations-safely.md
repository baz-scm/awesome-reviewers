---
title: Handle unsafe operations safely
description: Always wrap potentially unsafe operations (like JSON parsing, Buffer
  operations, or API calls) in try-catch blocks with appropriate error handling. Ensure
  error messages are user-friendly and actionable.
repository: continuedev/continue
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 27819
---

Always wrap potentially unsafe operations (like JSON parsing, Buffer operations, or API calls) in try-catch blocks with appropriate error handling. Ensure error messages are user-friendly and actionable.

Example:
```typescript
// Bad: Unsafe operation without error handling
const data = Buffer.from(input, "base64").toString("utf8");
const config = JSON.parse(toolCall.function.arguments);

// Good: Proper error handling with user-friendly messages
try {
  const data = Buffer.from(input, "base64").toString("utf8");
  return data;
} catch (error) {
  throw new Error("Invalid data format provided. Please check your input.");
}

try {
  const config = JSON.parse(toolCall.function.arguments);
  return config;
} catch (error) {
  throw new Error("Invalid configuration format. Please verify the syntax.");
}
```

Key points:
1. Identify potentially unsafe operations in your code
2. Always wrap them in try-catch blocks
3. Handle errors gracefully with appropriate recovery or fallback logic
4. Provide clear, user-friendly error messages that help users understand and resolve the issue
5. Avoid exposing technical details in user-facing error messages unless necessary