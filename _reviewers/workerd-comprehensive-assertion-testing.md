---
title: comprehensive assertion testing
description: Ensure test assertions are thorough and complete by testing both expected
  behavior and error conditions with specific error types and messages. Tests should
  cover edge cases, boundary conditions, and all relevant code branches rather than
  just happy path scenarios.
repository: cloudflare/workerd
label: Testing
language: JavaScript
comments_count: 7
repository_stars: 6989
---

Ensure test assertions are thorough and complete by testing both expected behavior and error conditions with specific error types and messages. Tests should cover edge cases, boundary conditions, and all relevant code branches rather than just happy path scenarios.

When using `assert.throws()`, always include a second argument to verify the specific error type and message:

```javascript
// Instead of just:
assert.throws(() => {
  env.ns.jurisdiction('foo');
});

// Do this:
assert.throws(() => {
  env.ns.jurisdiction('foo');
}, {
  code: 'ERR_INVALID_JURISDICTION',
  message: 'Invalid jurisdiction specified'
});
```

Test boundary conditions and edge cases systematically:
- Invalid input values (NaN, Infinity, out-of-range numbers)
- Both error and non-error scenarios for the same function
- Multiple variations of similar inputs (e.g., single vs multiple newlines)
- All code branches, including error handling paths

Use appropriate assertion methods for different scenarios - `assert.rejects()` for async operations that should fail, `assert.strictEqual()` for exact matches, and verify that expected ranges or types are properly validated rather than just checking for existence.