---
title: Handle async operations safely
description: Always wrap asynchronous operations in try-catch blocks to prevent unhandled
  promise rejections and provide graceful error recovery. This is especially important
  for browser APIs that may fail due to user permissions, network issues, or browser
  compatibility.
repository: cline/cline
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 48299
---

Always wrap asynchronous operations in try-catch blocks to prevent unhandled promise rejections and provide graceful error recovery. This is especially important for browser APIs that may fail due to user permissions, network issues, or browser compatibility.

When an async operation fails, log the error appropriately and implement fallback behavior or user-friendly error messages. Avoid letting async operations fail silently, as this can lead to confusing user experiences.

Example of proper async error handling:
```typescript
const handleCopyCode = async () => {
  try {
    await navigator.clipboard.writeText(code)
  } catch (err) {
    console.error('Copy failed', err)
    // Optional: Show user-friendly error message
  }
}
```

For operations that may fail but have acceptable fallback behavior, handle errors gracefully by returning default values and informing users when appropriate, such as showing "Chrome not detected" messages when browser detection fails.