---
title: safe error data handling
description: When processing error data that may contain unsafe or undefined values,
  use safe parsing methods and defensive programming techniques to prevent secondary
  exceptions during error handling.
repository: nuxt/nuxt
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 57769
---

When processing error data that may contain unsafe or undefined values, use safe parsing methods and defensive programming techniques to prevent secondary exceptions during error handling.

Use safe JSON parsing libraries like `destr()` instead of `JSON.parse()` when parsing potentially malformed JSON data from error objects:

```javascript
// Instead of:
ssrError.data = JSON.parse(ssrError.data)

// Use:
ssrError.data = destr(ssrError.data)
```

Apply destructuring with fallback values when accessing potentially undefined error data:

```javascript
// Instead of:
const caller = stack[stack.length - 1]
const explanation = `${fileURLToPath(caller.source)}:${caller.line}:${caller.column}`

// Use:
const {source, line, column} = stack[stack.length - 1] ?? {}
const explanation = source ? ` (used at ${fileURLToPath(source)}:${line}:${column})` : ''
```

This approach prevents error handling code from becoming a source of additional errors, ensuring that the original error information is preserved and properly communicated to users or logging systems.