---
title: coordinate concurrent initialization
description: When implementing expensive initialization operations that may be triggered
  concurrently, use a shared promise to coordinate multiple requests and prevent duplicate
  initialization. This pattern is especially important for operations like downloading
  dependencies, starting external processes, or establishing connections that take
  significant time to complete.
repository: sst/opencode
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 28213
---

When implementing expensive initialization operations that may be triggered concurrently, use a shared promise to coordinate multiple requests and prevent duplicate initialization. This pattern is especially important for operations like downloading dependencies, starting external processes, or establishing connections that take significant time to complete.

Store the initialization promise in a module-level variable and reuse it across concurrent calls. This ensures that multiple simultaneous requests will wait for the same initialization to complete rather than starting duplicate operations.

```typescript
let jdtlsInit: Promise<ChildProcessWithoutNullStreams | undefined>

async spawn(root) {
  // ... validation logic ...
  
  if (jdtlsInit == null) {
    jdtlsInit = initializeJdtls(java, root)
  }
  const jdtlsServer = await jdtlsInit
  
  // ... use initialized resource ...
}
```

This approach prevents race conditions where "initialization could run twice or more" due to the time-consuming nature of the operation, and allows concurrent requests to "wait for concurrent initialization requests until the first one's initialization is finished."