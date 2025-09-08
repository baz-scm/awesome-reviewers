---
title: Safe null handling
description: 'Always handle potentially null or undefined values defensively using
  appropriate JavaScript patterns. Choose the right technique based on your specific
  needs:'
repository: gravitational/teleport
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 19109
---

Always handle potentially null or undefined values defensively using appropriate JavaScript patterns. Choose the right technique based on your specific needs:

- Use optional chaining (`?.`) for safe property access when the object might be undefined
- Use nullish coalescing (`??`) for fallback values, but test thoroughly as it may not work as expected in all contexts
- Use explicit ternary operators (`value ? value : fallback`) when you need precise control over truthy/falsy behavior
- Use logical AND (`&&`) for conditional execution when you need to check existence before proceeding

Examples:
```javascript
// Optional chaining for safe property access
i.description?.toLowerCase().includes(s)

// Explicit ternary for reliable fallbacks
const desktop = desktop_name ? desktop_name : desktop_addr;

// When nullish coalescing works as expected
const value = input ?? defaultValue;
```

Choose the pattern that provides the clearest intent and most reliable behavior for your specific use case. Test edge cases to ensure your chosen approach handles empty strings, null, and undefined values as expected.