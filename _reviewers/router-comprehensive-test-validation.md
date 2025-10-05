---
title: comprehensive test validation
description: Tests should validate all relevant aspects of the system to ensure comprehensive
  coverage. This includes incorporating type checking into test execution, validating
  file operations and generation processes, and ensuring end-to-end functionality
  works correctly. Different types of tests serve different validation purposes and
  should be used strategically.
repository: TanStack/router
label: Testing
language: Json
comments_count: 2
repository_stars: 11590
---

Tests should validate all relevant aspects of the system to ensure comprehensive coverage. This includes incorporating type checking into test execution, validating file operations and generation processes, and ensuring end-to-end functionality works correctly. Different types of tests serve different validation purposes and should be used strategically.

For example, when running tests, include type checking alongside runtime tests:
```json
"scripts": {
  "test:lib": "vitest --typecheck"
}
```

Additionally, consider separate e2e tests when they validate distinct functionality like file reading, code generation, or navigation flows that unit tests might not cover. As one developer noted: "I wanted a test, without the `routeTree.gen.ts` committed into git so that on every CI run, it generated the `routeTree.gen.ts` from the `routes.ts` and ensured the navigations were successful."

This approach ensures that both compile-time correctness (through type checking) and runtime behavior (through comprehensive test scenarios) are validated, providing confidence in the system's reliability across different operational contexts.