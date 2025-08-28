---
title: Test comprehensive error scenarios
description: When implementing error handling, ensure comprehensive test coverage
  by testing multiple error scenarios, edge cases, and boundary conditions. Don't
  just test the happy path - validate that your code properly handles invalid inputs,
  out-of-range values, and error propagation.
repository: cloudflare/workerd
label: Error Handling
language: JavaScript
comments_count: 2
repository_stars: 6989
---

When implementing error handling, ensure comprehensive test coverage by testing multiple error scenarios, edge cases, and boundary conditions. Don't just test the happy path - validate that your code properly handles invalid inputs, out-of-range values, and error propagation.

Test cases should verify:
- Specific error codes and messages are returned correctly
- Custom error properties are preserved during propagation
- Edge cases like invalid values (NaN, Infinity, negative numbers, non-integers)
- Boundary conditions and out-of-range inputs
- Error state transitions (e.g., operations after stream end)

Example from the discussions:
```javascript
// Test multiple invalid port scenarios
for (const value of [NaN, Infinity, -1, -Infinity, 1.1, 9999999]) {
  // Test each invalid case
}

// Verify specific error codes
res.write('world', (err) => {
  strictEqual(err.code, 'ERR_STREAM_WRITE_AFTER_END');
});

// Test custom error properties are preserved
assert.strictEqual(e.abc, 123);
assert.strictEqual(e.stack.includes('at async Object.test'), true);
```

This approach ensures robust error handling that gracefully manages failure scenarios and provides meaningful feedback to users and developers.