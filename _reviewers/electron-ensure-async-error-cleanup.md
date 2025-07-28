---
title: Ensure async error cleanup
description: Always ensure cleanup code executes and avoid creating dangling promises
  in error handling scenarios. Use try-catch-finally patterns for guaranteed cleanup,
  and avoid making error handlers async unless you properly handle promise rejections.
repository: electron/electron
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 117644
---

Always ensure cleanup code executes and avoid creating dangling promises in error handling scenarios. Use try-catch-finally patterns for guaranteed cleanup, and avoid making error handlers async unless you properly handle promise rejections.

For test assertions and cleanup operations, collect data first, then perform assertions outside the error-prone section:

```javascript
// Good: Assertions run even if errors occur
const lines = [];
let handle = null;
try {
  handle = await fs.open(file);
  for await (const line of handle.readLines()) {
    lines.push(line);
  }
} finally {
  await handle?.close();
  await fs.rm(file, { force: true });
}
expect(lines.length).to.equal(1);
expect(lines[0]).to.equal('before exit');
```

For async operations, use try-catch-finally instead of making error handlers async:

```javascript
// Good: Proper cleanup with try-catch-finally
loadESM(async (esmLoader: any) => {
  try {
    await esmLoader.import(main, undefined, Object.create(null))
  } catch (e) {
    process.emit('uncaughtException', err);
  } finally {
    appCodeLoaded!();
  }
});

// Avoid: Making error handlers async creates dangling promises
capturer._onerror = (error: string) => {
  // Handle synchronously or use .then() for promises
  winsOwnedByElectronProcess.then(() => {
    stopRunning();
    reject(error);
  });
};
```

This pattern ensures that cleanup operations always execute and prevents unhandled promise rejections that can lead to application instability.