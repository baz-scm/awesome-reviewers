---
title: Prevent race conditions
description: When handling concurrent operations in asynchronous environments, avoid
  mutating shared state that could lead to race conditions. Instead, create operation-specific
  state or use immutable patterns to ensure each request path has isolated context.
repository: nestjs/nest
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 71766
---

When handling concurrent operations in asynchronous environments, avoid mutating shared state that could lead to race conditions. Instead, create operation-specific state or use immutable patterns to ensure each request path has isolated context.

**Problem example:**
```typescript
// PROBLEMATIC: Mutating shared socket instance can cause race conditions
Object.assign(socket, {
  getPattern: () => this.reflectCallbackPattern(currentCallback),
});
```

If multiple messages arrive nearly simultaneously, they could overwrite each other's metadata before processing completes.

**Better approach:**
```typescript
// Create request-specific context instead of modifying shared objects
class WsArgumentHost {
  constructor(private client: any, private callback: MessageHandler) {}
  
  getClient() {
    return this.client;
  }
  
  getPattern() {
    return this.reflectCallbackPattern(this.callback);
  }
}
```

Other best practices:
1. Use flags to check cancellation before performing resource allocation
2. Use Set or Map data structures to track execution state without side effects
3. Create local copies of data instead of modifying shared objects
4. Consider using immutable data structures for shared state