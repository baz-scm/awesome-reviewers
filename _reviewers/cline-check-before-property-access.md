---
title: Check before property access
description: Always verify that parent objects and properties exist before accessing
  nested properties or calling methods on them. Use optional chaining (`?.`) only
  when the parent object might genuinely be null or undefined, not as a blanket safety
  measure for guaranteed values. When values can be undefined, provide meaningful
  defaults rather than arbitrary fallbacks.
repository: cline/cline
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 48299
---

Always verify that parent objects and properties exist before accessing nested properties or calling methods on them. Use optional chaining (`?.`) only when the parent object might genuinely be null or undefined, not as a blanket safety measure for guaranteed values. When values can be undefined, provide meaningful defaults rather than arbitrary fallbacks.

**Good examples:**
```typescript
// When parent might be undefined
if (navigator && navigator.userAgent) {
    const isChrome = navigator.userAgent.indexOf("Chrome") >= 0
}

// When property might be undefined  
const cachedTokens = chunk.usage.prompt_tokens_details?.cached_tokens || 0

// When request is guaranteed to exist
if (request.options?.canSelectMany !== undefined) { // not request?.options
```

**Avoid:**
```typescript
// Unnecessary optional chaining on guaranteed values
request?.options?.canSelectMany // when request is never null

// Accessing without null checks
const isChrome = navigator.userAgent.indexOf("Chrome") >= 0 // navigator might be undefined

// Arbitrary defaults that cause calculation errors
let effectiveOutputPrice = modelInfo.outputPrice || 0 // should use meaningful default
```

This prevents runtime errors from null reference exceptions and ensures more predictable behavior when handling optional data.