---
title: validate post-manipulation state
description: Always explicitly validate object state after performing manipulations
  that could potentially result in null or undefined values. This is especially critical
  when dealing with global objects, parsing operations, or any transformation that
  might leave objects in an unexpected state.
repository: cloudflare/workerd
label: Null Handling
language: JavaScript
comments_count: 2
repository_stars: 6989
---

Always explicitly validate object state after performing manipulations that could potentially result in null or undefined values. This is especially critical when dealing with global objects, parsing operations, or any transformation that might leave objects in an unexpected state.

When manipulating global objects or performing parsing operations, include explicit assertions or checks to verify the object is in the expected state and hasn't become null or undefined:

```javascript
// Good: Explicit validation after global object manipulation
const originalProcess = process;
globalThis.process = 123;
assert.strictEqual(globalThis.process, 123); // Validate intermediate state
globalThis.process = originalProcess;
assert.strictEqual(globalThis.process, process); // Validate final restoration

// Good: Test edge cases in parsing that might produce null/undefined
const headers = parseHeaders('Content-Type: text/plain; f="a, b, \\"c\\""');
assert(headers['content-type'] !== null, 'Header should not be null after parsing');
assert(headers['content-type'] !== undefined, 'Header should be defined after parsing');
```

This practice prevents silent failures where objects become unexpectedly null or undefined, making issues immediately visible through explicit validation rather than allowing them to propagate and cause harder-to-debug problems downstream.