---
title: Wrap throwing operations
description: Always wrap potentially throwing operations in try/catch blocks to prevent
  unhandled exceptions from crashing the application or causing unexpected behavior.
  This includes property access on unknown objects, API calls, and resource initialization.
repository: cloudflare/workerd
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 6989
---

Always wrap potentially throwing operations in try/catch blocks to prevent unhandled exceptions from crashing the application or causing unexpected behavior. This includes property access on unknown objects, API calls, and resource initialization.

Many operations that appear safe can actually throw exceptions. Property access like `val.stack` can throw, method calls like `getReader()` can throw, and even seemingly simple operations may have hidden failure modes. Failing to catch these exceptions can lead to application crashes or inconsistent state.

Example of defensive error handling:

```typescript
// Before - risky property access
if (val && isObject && val.stack && typeof val.stack === 'string') {
  out.push(`Stack:\n${val.stack}`);
}

// After - defensive with try/catch
if (val && isObject && val.stack && typeof val.stack === 'string') {
  try {
    out.push(`Stack:\n${val.stack}`);
  } catch {
    // Ignore errors when accessing stack property
  }
}

// Before - risky method call
this.#reader ??= this._stream.getReader();
const data = await this.#reader.read();

// After - wrapped in try/catch
try {
  this.#reader ??= this._stream.getReader();
  const data = await this.#reader.read();
  // ... handle success
} catch (error) {
  this.destroy(error);
}
```

When catching exceptions, decide whether to ignore them silently, log them, or propagate them up the call stack based on the context and severity of the failure.