---
title: Comprehensive test coverage
description: Ensure comprehensive test coverage by systematically considering all
  scenarios, edge cases, and feature combinations when adding or modifying functionality.
  This includes testing both positive and negative cases, feature gate enabled/disabled
  states, error conditions, and boundary conditions.
repository: kubernetes/kubernetes
label: Testing
language: Go
comments_count: 16
repository_stars: 116489
---

Ensure comprehensive test coverage by systematically considering all scenarios, edge cases, and feature combinations when adding or modifying functionality. This includes testing both positive and negative cases, feature gate enabled/disabled states, error conditions, and boundary conditions.

When adding new functionality, ask yourself:
- Are all code paths tested, including error conditions?
- Are edge cases and boundary conditions covered?
- If feature gates are involved, are both enabled and disabled states tested?
- Are different parameter combinations and input variations tested?
- Do tests cover integration scenarios and not just isolated unit behavior?

For example, when adding CEL changes, don't just test the happy path - also test invalid expressions, edge cases in the evaluation logic, and integration with other components. When implementing backtracking algorithms, ensure tests cover scenarios where backtracking is actually triggered, not just cases where it succeeds on the first attempt.

```go
// Good: Comprehensive test coverage
func TestAllocatorBacktracking(t *testing.T) {
    testCases := []struct {
        name string
        // Test successful allocation
        // Test backtracking scenarios  
        // Test resource exhaustion
        // Test constraint violations
        // Test feature gate enabled/disabled
    }{
        {
            name: "successful allocation without backtracking",
            // ...
        },
        {
            name: "backtracking required due to constraint violation", 
            // ...
        },
        {
            name: "backtracking fails - no valid allocation",
            // ...
        },
    }
}
```

Incomplete test coverage often leads to production bugs that could have been caught during development. Take time to systematically think through all the ways your code could be exercised.