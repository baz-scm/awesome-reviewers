---
title: Never swallow errors
description: Always ensure errors are properly surfaced rather than silently ignored.
  Silent error handling can lead to confusing behavior where features fail without
  any indication of what went wrong, making debugging difficult or impossible.
repository: oven-sh/bun
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 79093
---

Always ensure errors are properly surfaced rather than silently ignored. Silent error handling can lead to confusing behavior where features fail without any indication of what went wrong, making debugging difficult or impossible.

There are several ways to properly handle errors instead of silently swallowing them:

1. Use logging channels to surface errors that aren't immediately user-facing:
```typescript
// Bad
try {
  await this.findTestFiles();
} catch (error) {
  // Silent error handling
}

// Good
try {
  await this.findTestFiles();
} catch (error) {
  this.outputChannel.appendLine(`Test discovery failed: ${error.message}`);
}
```

2. Maintain important assertions that validate input requirements:
```typescript
// Bad
export function isReadableStreamLocked(stream) {
  // $assert($isReadableStream(stream));  // Don't remove assertions!
}

// Good
export function isReadableStreamLocked(stream) {
  $assert($isReadableStream(stream));
}
```

3. Check return values from critical operations that may fail:
```typescript
// Bad
handle.init(initParamsArray, pledgedSrcSize, writeState, processCallback);

// Good
const initResult = handle.init(initParamsArray, pledgedSrcSize, writeState, processCallback);
if (initResult !== 0) {
  throw new Error(`Initialization failed with code ${initResult}`);
}
```

When errors are properly surfaced, developers can identify and fix issues more efficiently, leading to more robust and maintainable code.