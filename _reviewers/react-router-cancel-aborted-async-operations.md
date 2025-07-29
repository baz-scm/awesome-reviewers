---
title: Cancel aborted async operations
description: When working with async operations that can be aborted (like HTTP requests),
  ensure proper cancellation of related promises and deferred operations to prevent
  memory leaks and unnecessary work. This applies to both operations created after
  abortion has occurred and those created before abortion.
repository: remix-run/react-router
label: Concurrency
language: TypeScript
comments_count: 3
repository_stars: 55270
---

When working with async operations that can be aborted (like HTTP requests), ensure proper cancellation of related promises and deferred operations to prevent memory leaks and unnecessary work. This applies to both operations created after abortion has occurred and those created before abortion.

For operations created after abortion, check the abort signal before proceeding:
```typescript
let result = await handler(args);
if (args.request.signal.aborted && isDeferredData(result)) {
  result.cancel();
}
```

For operations created before abortion, set up abort listeners to handle cancellation:
```typescript
if (isDeferredData(result)) {
  if (request.signal.aborted) {
    result.cancel();
  } else {
    let deferResult = result;
    request.signal.addEventListener("abort", () => deferResult.cancel());
  }
}
```

This pattern prevents resource leaks and ensures that aborted requests don't continue consuming system resources. Always consider both the proactive case (already aborted) and reactive case (abort during execution) when implementing cancellation logic.