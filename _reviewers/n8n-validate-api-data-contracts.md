---
title: Validate API data contracts
description: Always validate API request and response data using schema validation
  to ensure type safety and prevent runtime errors. Define explicit schemas (e.g.,
  using Zod or similar) for all API interfaces rather than relying on TypeScript types
  alone.
repository: n8n-io/n8n
label: API
language: TypeScript
comments_count: 5
repository_stars: 122978
---

Always validate API request and response data using schema validation to ensure type safety and prevent runtime errors. Define explicit schemas (e.g., using Zod or similar) for all API interfaces rather than relying on TypeScript types alone.

Example:
```typescript
// Before
interface ChatMessage {
  action: string;
  chatInput: string;
  sessionId: string;
}

async function handleMessage(data: RawData) {
  const message = jsonParse<ChatMessage>(data.toString());
  // No validation, could fail at runtime
  await processMessage(message);
}

// After
const chatMessageSchema = z.object({
  action: z.enum(['user', 'system']),
  chatInput: z.string(),
  sessionId: z.string().uuid()
});

type ChatMessage = z.infer<typeof chatMessageSchema>;

async function handleMessage(data: RawData) {
  const rawMessage = jsonParse(data.toString());
  const message = chatMessageSchema.parse(rawMessage);
  // Validated data, guaranteed to match schema
  await processMessage(message);
}
```

This practice:
- Catches invalid data early before it causes downstream errors
- Provides clear documentation of expected data structures
- Ensures runtime type safety beyond TypeScript's compile-time checks
- Makes API contracts explicit and self-documenting