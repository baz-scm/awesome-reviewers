---
title: Descriptive behavior-based tests
description: Tests should be named to describe the expected behavior or outcome being
  verified, not the input parameters or implementation details. This makes tests more
  meaningful as documentation and easier to understand when they fail.
repository: nodejs/node
label: Testing
language: Other
comments_count: 2
repository_stars: 112178
---

Tests should be named to describe the expected behavior or outcome being verified, not the input parameters or implementation details. This makes tests more meaningful as documentation and easier to understand when they fail.

When writing test names:
- Describe what functionality is being tested
- Focus on the expected outcome or behavior
- Use a "when X, then Y" pattern when appropriate

Instead of:
```javascript
test('help arg value config must be a string', () => {
  // Test code
});
```

Prefer:
```javascript
test('when help option receives non-string value, then throws type error', () => {
  // Test code
});
```

Tests should also have exactly one expected outcome without conditional assertions. This ensures deterministic tests that clearly indicate what behavior is considered correct.

Avoid:
```javascript
if (stderr) {
  // One assertion path
} else {
  // Different assertion path
}
```

Instead, be explicit about what the test expects:
```javascript
strictEqual(stderr, '');
strictEqual(stdout, 'exports require module __filename __dirname\n');
```