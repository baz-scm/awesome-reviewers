---
title: Operation order affects correctness
description: When implementing algorithms that involve multiple operations (like iteration,
  validation, and execution), the order of operations can critically affect correctness.
  Always validate operation ordering to ensure no unintended side effects or lost
  data.
repository: temporalio/temporal
label: Algorithms
language: Go
comments_count: 3
repository_stars: 14953
---

When implementing algorithms that involve multiple operations (like iteration, validation, and execution), the order of operations can critically affect correctness. Always validate operation ordering to ensure no unintended side effects or lost data.

Key considerations:
1. Iterator consumption should be checked before boundary conditions
2. Validation and execution of dependent items must be interleaved
3. State changes that affect validation must be processed sequentially

Example of correct iterator usage:
```go
// Good: Check boundary before consuming iterator
for b := 0; b < batchSize && it.Next(); b++ {
    // Process item
}

// Bad: May consume item that gets dropped
for b := 0; it.Next() && b < batchSize; b++ {
    // Process item
}
```

For validation/execution sequences:
```go
// Good: Interleave validation and execution
for _, task := range tasks {
    valid, err := validateTask(task)
    if err != nil || !valid {
        continue
    }
    err = executeTask(task) // Execute immediately after validation
}

// Bad: Separate validation from execution
validTasks := []Task{}
for _, task := range tasks {
    valid, _ := validateTask(task)
    if valid {
        validTasks = append(validTasks, task)
    }
}
for _, task := range validTasks {
    executeTask(task) // Task may be invalid now due to previous executions
}
```