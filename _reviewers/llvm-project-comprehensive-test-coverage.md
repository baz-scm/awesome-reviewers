---
title: comprehensive test coverage
description: 'Tests should comprehensively cover all relevant scenarios, including
  return values, edge cases, different compilation modes, and abnormal conditions.
  This includes:'
repository: llvm/llvm-project
label: Testing
language: C++
comments_count: 7
repository_stars: 33702
---

Tests should comprehensively cover all relevant scenarios, including return values, edge cases, different compilation modes, and abnormal conditions. This includes:

1. **Return Value Testing**: Always verify function return values rather than ignoring them. For example, instead of just calling `pthread_barrier_wait(&barrier)`, check the return value and assert expected behavior:
```cpp
int result = LIBC_NAMESPACE::pthread_barrier_wait(&barrier);
if (result == PTHREAD_BARRIER_SERIAL_THREAD) {
  serial_counter.fetch_add(1);
} else {
  ASSERT_EQ(result, 0);
}
```

2. **Edge Case Coverage**: Add tests for abnormal scenarios like address capturing, incorrect function signatures, and boundary conditions that might not occur in normal usage but could reveal bugs.

3. **Multi-Mode Testing**: When applicable, test across different compilation modes (host/device, different C++ standards) to ensure functionality works consistently:
```cpp
// RUN: %clang_cc1 -fsycl-is-host -fsyntax-only -verify %s
// RUN: %clang_cc1 -fsycl-is-device -fsyntax-only -verify %s
```

4. **Coverage Analysis**: Use coverage tools to identify untested branches and remove or test unreachable code paths. Functions with many branches should have their coverage verified to ensure all paths are exercised.

5. **Language Feature Testing**: Include tests for relevant language features like `constexpr`, `consteval`, and other constructs that might interact with the code being tested.

This approach helps catch bugs that might only manifest in specific scenarios and ensures robust, reliable code across different environments and use cases.