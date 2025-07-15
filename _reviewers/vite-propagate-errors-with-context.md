---
title: Propagate errors with context
description: Always propagate errors with proper context and recovery strategy. Use
  try-catch blocks for both synchronous and asynchronous operations, ensure error
  information is preserved, and provide meaningful error messages.
repository: vitejs/vite
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 74031
---

Always propagate errors with proper context and recovery strategy. Use try-catch blocks for both synchronous and asynchronous operations, ensure error information is preserved, and provide meaningful error messages.

Key practices:
1. Use try-catch over existence checks
2. Preserve error context in async chains
3. Include source information and frames
4. Implement recovery strategies where appropriate

Example:
```typescript
// Instead of:
if (fs.existsSync(srcFile)) {
  const stats = fs.statSync(srcFile)
}

// Do:
try {
  const stats = fs.statSync(srcFile)
} catch (e) {
  if (e.code === 'ENOENT') {
    // Handle missing file case
  }
  // Preserve context and rethrow
  throw new Error(`Failed to read ${srcFile}: ${e.message}`, { cause: e })
}

// For async handlers:
async function middleware(req, res, next) {
  try {
    await processRequest(req)
  } catch (e) {
    // Add context and pass to error handler
    e.url = req.url
    e.frame = generateCodeFrame(e.pos)
    return next(e)
  }
}
```