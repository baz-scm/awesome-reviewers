---
title: Manage output streams carefully
description: Always consider the destination and lifecycle of output streams to prevent
  protocol interference, data loss, and unexpected behavior. Choose stdout for application
  output and stderr for debugging/logging. Avoid accidentally closing streams and
  be mindful of output pollution in protocol-sensitive contexts.
repository: prisma/prisma
label: Logging
language: TypeScript
comments_count: 6
repository_stars: 42967
---

Always consider the destination and lifecycle of output streams to prevent protocol interference, data loss, and unexpected behavior. Choose stdout for application output and stderr for debugging/logging. Avoid accidentally closing streams and be mindful of output pollution in protocol-sensitive contexts.

Key practices:
- Use stderr for debug/log output to avoid interfering with application protocols
- When piping streams, use `{ end: false }` option to prevent closing the target stream
- In protocol-sensitive contexts (like JSON-RPC), redirect console output to stderr to prevent stdout pollution
- Prefer `process.stderr.write` over `console.warn` in tests to avoid mock interference
- Use `console.error.bind(console)` instead of custom implementations to preserve formatting

Example:
```typescript
// Good: Prevent stdout closure when piping
fileStream.pipe(process.stdout, { end: false })

// Good: Redirect console in protocol contexts  
if (process.argv.includes('mcp')) {
  console.log = console.error.bind(console)
}

// Good: Use stderr for debug output
console.warn(`${namespace} ${format}`, ...rest)
```