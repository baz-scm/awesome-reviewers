---
title: Use parameterized testing
description: When testing multiple scenarios with similar logic, use your testing
  framework's built-in parameterized testing features (`test.each`, `describe.each`,
  `it.each`) instead of manual `forEach` loops or duplicated test functions. This
  approach reduces code duplication, improves readability, and makes it easier to
  add new test cases.
repository: TanStack/router
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 11590
---

When testing multiple scenarios with similar logic, use your testing framework's built-in parameterized testing features (`test.each`, `describe.each`, `it.each`) instead of manual `forEach` loops or duplicated test functions. This approach reduces code duplication, improves readability, and makes it easier to add new test cases.

Instead of writing repetitive test functions or using manual iteration:

```ts
// ❌ Avoid manual forEach loops
[
  { path: '/', expected: undefined },
  { path: '/single', expected: '/single' },
  { path: '/path/example', expected: '/example' }
].forEach(({ path, expected }) => {
  it(`should handle ${path}`, () => {
    expect(getLastPathSegment(path)).toBe(expected)
  })
})
```

Use the framework's parameterized testing features:

```ts
// ✅ Use test.each for cleaner parameterized tests
it.each([
  ['/', undefined, 'root path'],
  ['/single', '/single', 'single segment'],
  ['/path/example', '/example', 'multiple segments']
])('should return %s for path %s (%s)', (path, expected, description) => {
  expect(getLastPathSegment(path)).toBe(expected)
})
```

This pattern works well for testing multiple input/output combinations, different browser scenarios, or various configuration states. It makes tests more maintainable and provides clearer test output when failures occur.