---
title: Write comprehensive test cases
description: 'Tests should thoroughly cover all code paths and edge cases. Each test
  case should:

  1. Test distinct scenarios in separate test cases

  2. Cover all logical branches and code paths'
repository: vuejs/core
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 50769
---

Tests should thoroughly cover all code paths and edge cases. Each test case should:
1. Test distinct scenarios in separate test cases
2. Cover all logical branches and code paths
3. Use clear, specific test names that describe the scenario being tested
4. Include both positive and negative test cases

Example:
```js
// ❌ Incomplete test coverage
test('isRef check', () => {
  expect(isRef(computed(() => 1))).toBe(true)
})

// ✅ Comprehensive test coverage
describe('isRef', () => {
  test('returns true for computed values', () => {
    expect(isRef(computed(() => 1))).toBe(true)
  })

  test('returns false for primitive values', () => {
    expect(isRef(0)).toBe(false)
    expect(isRef(1)).toBe(false)  // Test truthy primitive
    expect(isRef('')).toBe(false) // Test falsy primitive
  })
  
  test('returns true for ref values', () => {
    expect(isRef(ref(1))).toBe(true)
    expect(isRef(ref(null))).toBe(true)
  })
})
```