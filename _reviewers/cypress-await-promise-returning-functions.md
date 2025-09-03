---
title: await promise-returning functions
description: Always await functions that return promises to ensure proper asynchronous
  execution and avoid potential race conditions or unexpected behavior. When converting
  from promise chains to async/await, verify that all promise-returning function calls
  include the await keyword.
repository: cypress-io/cypress
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 48850
---

Always await functions that return promises to ensure proper asynchronous execution and avoid potential race conditions or unexpected behavior. When converting from promise chains to async/await, verify that all promise-returning function calls include the await keyword.

Common mistake: Calling a promise-returning function without await, which can lead to unhandled promises and timing issues.

```ts
// ❌ Incorrect - missing await
export const showDialogAndCreateSpec = async () => {
  const cfg = openProject.getConfig()
  const path = await showSaveDialog(cfg.integrationFolder)
  
  if (path) {
    createFile(path) // Missing await - promise not handled
  }
}

// ✅ Correct - properly awaited
export const showDialogAndCreateSpec = async () => {
  const cfg = openProject.getConfig()
  const path = await showSaveDialog(cfg.integrationFolder)
  
  if (path) {
    await createFile(path) // Properly awaited
  }
}
```

This is especially important when refactoring from promise chains (.then()) to async/await syntax, as it's easy to overlook promise-returning functions that need to be awaited.