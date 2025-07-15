---
title: Proper asynchronous error handling
description: Ensure errors in asynchronous operations and event-based systems are
  handled consistently to prevent unexpected behavior. Always maintain Promise integrity
  by never resolving and rejecting the same Promise, and use appropriate error event
  handlers.
repository: nestjs/nest
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 71767
---

Ensure errors in asynchronous operations and event-based systems are handled consistently to prevent unexpected behavior. Always maintain Promise integrity by never resolving and rejecting the same Promise, and use appropriate error event handlers.

When working with Promises:
```typescript
// INCORRECT: Could both reject and resolve the same promise
if (err instanceof KafkaRetriableException && !isPromiseResolved) {
  reject(err);
}

// CORRECT: Ensure mutual exclusivity
if (err instanceof KafkaRetriableException && !isPromiseResolved) {
  reject(err);
} else {
  // other code
}
```

For event streams and emitters:
```typescript
// INCORRECT: Using .on() may trigger multiple error handling instances
body.getStream().on('error', (err: Error) => {
  // This could be called multiple times, causing "headers already sent" errors
});

// CORRECT: Use .once() for one-time error events
body.getStream().once('error', (err: Error) => {
  // This will only be called once
});
```

For reactive streams, handle errors properly with catchError:
```typescript
result$.pipe(
  takeUntil(fromEvent(call, CANCEL_EVENT)),
  catchError(err => {
    const data = err instanceof Error ? err.message : err;
    stream.writeMessage({ type: 'error', data }, handleWriteError);
    return EMPTY; // or of(fallbackValue) depending on your recovery strategy
  })
)
```

Always ensure error handling preserves system consistency and properly releases resources. For critical errors, implement graceful shutdown mechanisms to prevent resource leaks and data corruption.