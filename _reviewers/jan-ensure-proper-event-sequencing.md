---
title: Ensure proper event sequencing
description: When working with event-driven systems, ensure that events are emitted
  at the appropriate time and in the correct context to prevent race conditions and
  incorrect behavior. Consider whether the function's purpose aligns with event emission
  - single-response functions should not broadcast events meant for streaming contexts.
  Additionally, be mindful of...
repository: menloresearch/jan
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 37620
---

When working with event-driven systems, ensure that events are emitted at the appropriate time and in the correct context to prevent race conditions and incorrect behavior. Consider whether the function's purpose aligns with event emission - single-response functions should not broadcast events meant for streaming contexts. Additionally, be mindful of timing when handling sequential operations to avoid race conditions.

For example, avoid emitting events in non-streaming contexts:
```typescript
// Bad: Emitting events in single-response function
const message = {
  status: MessageStatus.Pending,
  // ... other properties
};
events.emit(MessageEvent.OnMessageResponse, message); // Inappropriate for single-response

// Good: Only emit events in appropriate streaming contexts
if (isStreamingMode) {
  events.emit(MessageEvent.OnMessageResponse, message);
}
```

When handling sequential operations, ensure proper timing:
```typescript
// Bad: Potential race condition
if (messages.length == 1) {
  // Handle first message logic here - race condition possible
}

// Good: Handle after message response to avoid race
// Move to EventHandler > OnMessageResponse to ensure proper sequencing
```