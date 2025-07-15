---
title: Prevent async race conditions
description: 'Design async operations to prevent race conditions, memory leaks, and
  ensure proper resource cleanup. Key principles:


  1. Avoid mutating shared state in async operations'
repository: nestjs/nest
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 71767
---

Design async operations to prevent race conditions, memory leaks, and ensure proper resource cleanup. Key principles:

1. Avoid mutating shared state in async operations
2. Ensure proper cleanup of resources when async operations complete or are cancelled
3. Use appropriate data structures for async streaming to prevent event loop blocking

Example of problematic code:
```typescript
// BAD: Mutating shared state in async context
Object.assign(socket, {
  getPattern: () => this.reflectPattern(callback)
});

// BAD: Potential memory leak with async timing
this.routingMap.set(packet.id, callback);
await this.serialize(packet.data);
```

Better approach:
```typescript
// GOOD: Maintain request-scoped state
class RequestContext {
  constructor(private pattern: string) {}
  getPattern() { return this.pattern; }
}

// GOOD: Ensure cleanup on unsubscribe
const cleanup = new AbortController();
try {
  if (cleanup.signal.aborted) return;
  const data = await this.serialize(packet.data);
  this.routingMap.set(packet.id, callback);
  cleanup.signal.addEventListener('abort', () => {
    this.routingMap.delete(packet.id);
  });
} catch (err) {
  this.routingMap.delete(packet.id);
}
```

For streaming operations, use appropriate async scheduling:
```typescript
// GOOD: Non-blocking stream processing
return from(items).pipe(
  concatMap(item => defer(() => processItem(item))),
  observeOn(asyncScheduler)
);
```