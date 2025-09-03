---
title: Safe null access patterns
description: Always provide fallbacks when accessing properties or methods on values
  that could be undefined or null to prevent runtime errors. Use defensive programming
  patterns like logical OR operators, conditional checks, or nullish coalescing when
  available.
repository: cypress-io/cypress
label: Null Handling
language: Other
comments_count: 2
repository_stars: 48850
---

Always provide fallbacks when accessing properties or methods on values that could be undefined or null to prevent runtime errors. Use defensive programming patterns like logical OR operators, conditional checks, or nullish coalescing when available.

Examples of unsafe patterns:
```javascript
// Unsafe - could throw if renderProps is undefined
const showMarkdown = computed(() => props.command.renderProps && props.command.renderProps.message)

// Unsafe - could throw if message/markdown is undefined
scaled: computed(() => (props.message || props.markdown).length > 100)
```

Examples of safe patterns:
```javascript
// Safe - provides fallback value
const showMarkdown = computed(() => props.command.renderProps?.message ?? false)
// Or without optional chaining:
const showMarkdown = computed(() => props.command.renderProps && props.command.renderProps.message || false)

// Safe - provides empty string fallback
scaled: computed(() => (props.message || props.markdown || '').length > 100)
```

This prevents common runtime errors like "Cannot read property 'x' of undefined" and makes code more robust when dealing with optional or potentially missing data.